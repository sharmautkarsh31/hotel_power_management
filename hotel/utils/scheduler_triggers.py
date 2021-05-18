import os
from datetime import timedelta

from django.conf import settings
from django.utils.timezone import now
from django_apscheduler.models import DjangoJobExecution

from hotel.models import Light, AirConditioner, MotionDetection, SubCorridor


class TriggerActions():

    @staticmethod
    def night_shift_start_trigger():
        # Turning on night shift
        settings.NIGHT_SHIFT_ACTIVE = True

        # Turning on all lights and AC in the main corridor
        Light.objects.filter(main_corridor__isnull=False).update(turned_on=True)
        AirConditioner.objects.filter(main_corridor__isnull=False).update(turned_on=True)

        # Turning off all lights and turning on all ac in the sub corridor
        Light.objects.filter(sub_corridor__isnull=False).update(turned_on=False)
        AirConditioner.objects.filter(sub_corridor__isnull=False).update(turned_on=True)


    @staticmethod
    def night_shift_end_trigger():
        # Turning off night shift
        settings.NIGHT_SHIFT_ACTIVE = False

        # Turning off all lights
        Light.objects.all().update(turned_on=False)

        # Turning on all ACs
        AirConditioner.objects.all().update(turned_on=True)

    @staticmethod
    def motion_detection_trigger():
        if settings.NIGHT_SHIFT_ACTIVE:

            # action on new movements
            motion_detection_objs = MotionDetection.objects.filter(motion_timestamp__gte=now() -
                                                              timedelta(seconds=settings.LIGHTS_TURN_ON_INTERVAL))
            if motion_detection_objs.exists():

                TriggerActions.motion_detection_action(motion_detection_objs)
                # action 1 taken on motion detection

            # action on movements after LIGHTS_TURN_ON_INTERVAL.
            reverse_action_motion_detection_objs = MotionDetection.objects.filter(
                action_taken=False,
                motion_timestamp__lt=now() - timedelta(seconds=settings.LIGHTS_TURN_ON_INTERVAL)
            )

            sub_corridors_to_be_revereted = reverse_action_motion_detection_objs.values_list(
                'sub_corridor', flat=True)
            sub_corridors_with_recent_motion = motion_detection_objs.values_list('sub_corridor', flat=True)

            # Eliminating sub-corridors where someone passed between the LIGHTS_TURN_ON_INTERVAL.
            actual_corridors_for_reverse_action = set(sub_corridors_to_be_revereted) - set(sub_corridors_with_recent_motion)

            if len(actual_corridors_for_reverse_action):  # LIGHTS_TURN_ON_INTERVAL has been passed after the action has been taken

                TriggerActions.reverse_motion_detection_action(actual_corridors_for_reverse_action)

                # reverse action taken on motion detection
                reverse_action_motion_detection_objs.update(action_taken=True)

            if not settings.EXTREME_SAVER:
                # running ac for some time to maintain cooling and also keeping the bill in budget provided.
                # Currently turned off
                TriggerActions.maintain_cooling()
        else:
            TriggerActions.night_shift_end_trigger()

    @staticmethod
    def motion_detection_action(motion_detection_objs):
        # turning lights on
        lights = motion_detection_objs.values_list('sub_corridor__light', flat=True)
        Light.objects.filter(id__in=lights).update(turned_on=True)

        # turning ac off
        ac = motion_detection_objs.values_list('sub_corridor__airconditioner', flat=True)
        AirConditioner.objects.filter(id__in=ac).update(turned_on=False)

    @staticmethod
    def reverse_motion_detection_action(sub_corridors_ids):
        # turning lights off
        sub_corridors = SubCorridor.objects.filter(id__in=sub_corridors_ids)
        lights = sub_corridors.values_list('light', flat=True)
        Light.objects.filter(id__in=lights).update(turned_on=False)

        # turning ac on
        ac = sub_corridors.values_list('airconditioner', flat=True)
        AirConditioner.objects.filter(id__in=ac).update(turned_on=True)


    @staticmethod
    def maintain_cooling():
        # Keeping AC on for first 5 minutes of the every 10 minutes to maintain cooling
        if (now().minute) % 10 < 5 and AirConditioner.objects.filter(sub_corridor__isnull=False,
                                                                     turned_on=False).exists():
            # Running update statememt only when required i.e. only when already turned off
            AirConditioner.objects.filter(sub_corridor__isnull=False).update(turned_on=True)

    @staticmethod
    def delete_old_job_executions(max_age=604_800):
        """This job deletes all apscheduler job executions older than `max_age` from the database."""
        DjangoJobExecution.objects.delete_old_job_executions(max_age)
        MotionDetection.objects.filter(action_timestamp__lt=now() - timedelta(weeks=1)).delete()
