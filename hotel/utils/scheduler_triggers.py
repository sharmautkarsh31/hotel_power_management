import os
from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django_apscheduler.models import DjangoJobExecution

from hotel.models import MotionDetection, Floor, FloorPowerConsumptionPerHour, Appliance, ApplianceType, Corridor

units_consumed_per_second_factor = 1/3600

class TriggerActions():

    @staticmethod
    def check_floor_power_consumption_per_hour():
        if settings.NIGHT_SHIFT_ACTIVE:
            for floor in Floor.objects.all():
                power_consumption = TriggerActions.meter_power_consumption_per_hour(floor)

                # check if limit consumption exceeded
                TriggerActions.power_consumption_limit_breach(floor, power_consumption)
        else:
            # No action required
            pass

    @staticmethod
    def power_consumption_limit_breach(floor, power_consumption):
        floor_maincorridors = Corridor.objects.filter(corridor_type__type='MAIN_CORRIDOR',floor=floor)
        floor_subcorridors = Corridor.objects.filter(corridor_type__type='SUB_CORRIDOR',floor=floor)
        if power_consumption.units_consumed >= (
                floor_maincorridors.count() * settings.MAIN_CORRIDOR_UNIT_CONSUMPTION_LIMIT) + \
                (floor_subcorridors.count() * settings.SUB_CORRIDOR_UNIT_CONSUMPTION_LIMIT) - \
                (floor_subcorridors.count() * ApplianceType.objects.get(type='LIGHT').power_consumption_unit):
            floor.extreme_power_saver = True
            floor.save()

            # turn off all ACs of the subcorridor
            Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',corridor__in=floor_subcorridors).update(turned_on=False)
        else:
            floor.extreme_power_saver = False
            floor.save()

    @staticmethod
    def meter_power_consumption_per_hour(floor):
        sub_corridor_lights_count = Appliance.objects.filter(appliance_type__type='LIGHT',corridor__corridor_type__type='SUB_CORRIDOR',corridor__floor=floor,turned_on=True).count()
        sub_corridor_ac_count = Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',corridor__corridor_type__type='SUB_CORRIDOR',corridor__floor=floor,turned_on=True).count()
        main_corridor_lights_count = Appliance.objects.filter(appliance_type__type='LIGHT',corridor__corridor_type__type='MAIN_CORRIDOR', corridor__floor=floor,turned_on=True).count()
        main_corridor_ac_count = Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',corridor__corridor_type__type='MAIN_CORRIDOR', corridor__floor=floor,turned_on=True).count()
        power_consumption_per_second = (
                                           (sub_corridor_lights_count + main_corridor_lights_count) * ApplianceType.objects.get(type='LIGHT').power_consumption_unit +
                                           (sub_corridor_ac_count + main_corridor_ac_count) * ApplianceType.objects.get(type='AIR_CONDITIONER').power_consumption_unit
                                       ) * units_consumed_per_second_factor
        hour_of_the_day = now().hour
        power_consumption, _ = FloorPowerConsumptionPerHour.objects.get_or_create(floor=floor,
                                                                                  hour_of_day=hour_of_the_day)
        power_consumption.units_consumed += power_consumption_per_second
        power_consumption.save()
        return power_consumption

    @staticmethod
    def motion_detection_trigger():
        if settings.NIGHT_SHIFT_ACTIVE:

            # action on new movements
            motion_detection_objs = TriggerActions.action_on_new_movements()

            # action on movements after LIGHTS_TURN_ON_INTERVAL.
            TriggerActions.revert_state_after_interval(motion_detection_objs)

        else:
            TriggerActions.night_shift_end_trigger()

    @staticmethod
    def action_on_new_movements():
        motion_detection_objs = MotionDetection.objects.filter(motion_timestamp__gte=now() -
                                                                                     timedelta(
                                                                                         seconds=settings.LIGHTS_TURN_ON_INTERVAL))
        if motion_detection_objs.exists():
            TriggerActions.motion_detection_action(motion_detection_objs)
        return motion_detection_objs

    @staticmethod
    def revert_state_after_interval(motion_detection_objs):
        reverse_action_motion_detection_objs = MotionDetection.objects.filter(
            action_taken=False,
            motion_timestamp__lt=now() - timedelta(seconds=settings.LIGHTS_TURN_ON_INTERVAL)
        )
        sub_corridors_to_be_revereted = reverse_action_motion_detection_objs.values_list('corridor', flat=True)
        sub_corridors_with_recent_motion = motion_detection_objs.values_list('corridor', flat=True)

        # Eliminating sub-corridors where someone passed between the LIGHTS_TURN_ON_INTERVAL.
        actual_corridors_for_reverse_action = set(sub_corridors_to_be_revereted) - set(sub_corridors_with_recent_motion)

        if len(actual_corridors_for_reverse_action):  # LIGHTS_TURN_ON_INTERVAL has been passed after the action has been taken

            TriggerActions.reverse_motion_detection_action(actual_corridors_for_reverse_action)

            # reverse action taken on motion detection
            reverse_action_motion_detection_objs.update(action_taken=True)

    @staticmethod
    def motion_detection_action(motion_detection_objs):
        # turning lights on
        Appliance.objects.filter(appliance_type__type='LIGHT',
                                 corridor__corridor_type__type='SUB_CORRIDOR',
                                 corridor_id__in=motion_detection_objs.values_list('corridor_id')
                                 ).update(turned_on=True)

        # turning ac off
        Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',
                                 corridor__floor__extreme_power_saver=False,
                                 corridor__corridor_type__type='SUB_CORRIDOR',
                                 corridor_id__in=motion_detection_objs.values_list('corridor_id')
                                 ).update(turned_on=False)

    @staticmethod
    def reverse_motion_detection_action(sub_corridors_ids):
        # turning lights off
        Appliance.objects.filter(appliance_type__type='LIGHT',
                                          corridor__corridor_type__type='SUB_CORRIDOR',
                                          corridor_id__in=sub_corridors_ids,
                                          ).update(turned_on=False)

        # turning ac on

        Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',
                                 corridor__floor__extreme_power_saver=False,
                                 corridor__corridor_type__type='SUB_CORRIDOR',
                                 corridor_id__in=sub_corridors_ids
                                 ).update(turned_on=True)


    @staticmethod
    def night_shift_start_trigger():
        # Turning on night shift
        settings.NIGHT_SHIFT_ACTIVE = True

        # Turning on all lights and AC in the main corridor
        Appliance.objects.filter(appliance_type__type='LIGHT',corridor__corridor_type__type='MAIN_CORRIDOR').update(turned_on=True)
        Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',corridor__corridor_type__type='MAIN_CORRIDOR').update(turned_on=True)

        # Turning off all lights and turning on all ac in the sub corridor
        Appliance.objects.filter(appliance_type__type='LIGHT',corridor__corridor_type__type='SUB_CORRIDOR').update(turned_on=False)
        Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER',corridor__corridor_type__type='SUB_CORRIDOR').update(turned_on=True)


    @staticmethod
    def night_shift_end_trigger():
        # Turning off night shift
        settings.NIGHT_SHIFT_ACTIVE = False

        # Turning off all lights
        Appliance.objects.filter(appliance_type__type='LIGHT').update(turned_on=False)

        # Turning on all ACs
        Appliance.objects.filter(appliance_type__type='AIR_CONDITIONER').update(turned_on=True)


    @staticmethod
    def delete_old_job_executions(max_age=604_800):
        """This job deletes all apscheduler job executions older than `max_age` from the database."""
        DjangoJobExecution.objects.delete_old_job_executions(max_age)
        MotionDetection.objects.filter(action_timestamp__lt=now() - timedelta(weeks=1)).delete()
