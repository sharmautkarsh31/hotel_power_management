import random
from time import sleep

from django.test import TestCase, override_settings
from django.utils.timezone import now

from hotel.models import Light, AirConditioner, FloorPowerConsumptionPerHour, Floor, SubCorridor
from hotel.utils.scheduler_triggers import TriggerActions
from django.conf import settings

@override_settings(NIGHT_SHIFT_ACTIVE=True)
class TestTriggerMotionAPI(TestCase):

    def setUp(self) -> None:
        self.hotel_name = 'Test Hotel'
        self.floors = 2
        self.sub_corridors_per_floor = 2
        self.main_corridors_per_floor = 1
        self.create_hotel_data()
        self.floor = Floor.objects.first()

    def create_hotel_data(self):
        url = '/api/hotel/'
        payload = {
            "hotel_name": self.hotel_name,
            "floors": self.floors,
            "main_corridors": self.main_corridors_per_floor,
            "sub_corridors": self.sub_corridors_per_floor
        }
        self.client.post(url, data=payload, content_type='application/json')

    def test_turn_extreme_power_saver_on(self):
        self.floor.extreme_power_saver = False
        self.floor.save()

        light = Light.objects.filter(sub_corridor__floor=self.floor).first(); light.turned_on = False; light.save()
        ac = AirConditioner.objects.filter(sub_corridor__floor=self.floor).first(); ac.turned_on = True; ac.save()

        hour_of_the_day = now().hour
        units_consumed = self.sub_corridors_per_floor*settings.SUB_CORRIDOR_UNIT_CONSUMPTION_LIMIT + \
                         self.main_corridors_per_floor*settings.MAIN_CORRIDOR_UNIT_CONSUMPTION_LIMIT

        FloorPowerConsumptionPerHour.objects.create(floor=self.floor,
                                                    hour_of_day=hour_of_the_day,
                                                    units_consumed=units_consumed)

        TriggerActions.check_floor_power_consumption_per_hour()

        assert Floor.objects.first().extreme_power_saver==True
        assert AirConditioner.objects.filter(sub_corridor__floor=self.floor).first().turned_on==False

    def test_turn_extreme_power_saver_off(self):
        self.floor.extreme_power_saver = True
        self.floor.save()

        hour_of_the_day = now().hour
        units_consumed = 0.0

        FloorPowerConsumptionPerHour.objects.create(floor=self.floor,
                                                    hour_of_day=hour_of_the_day,
                                                    units_consumed=units_consumed)

        TriggerActions.check_floor_power_consumption_per_hour()

        assert Floor.objects.first().extreme_power_saver==False

    def test_motion_detection_action_extreme_power_saver_off(self):
        self.floor.extreme_power_saver = False
        self.floor.save()

        light = Light.objects.filter(sub_corridor__floor=self.floor).first()
        ac = AirConditioner.objects.filter(sub_corridor__floor=self.floor).first()

        light.turned_on = False
        light.save()

        ac.turned_on = True
        ac.save()

        payload = {
            "sub_corridor": SubCorridor.objects.filter(floor=self.floor).first().id
        }
        # create motion
        self.client.post('/api/trigger_motion/', data=payload, content_type='application/json')

        TriggerActions.motion_detection_trigger()

        assert Light.objects.filter(sub_corridor__floor=self.floor).first().turned_on==True
        assert AirConditioner.objects.filter(sub_corridor__floor=self.floor).first().turned_on==False

    @override_settings(LIGHTS_TURN_ON_INTERVAL=2)
    def test_motion_detection_action_extreme_power_saver_on(self):
        self.floor.extreme_power_saver = True
        self.floor.save()

        light = Light.objects.filter(sub_corridor__floor=self.floor).first(); light.turned_on = False; light.save()
        ac = AirConditioner.objects.filter(sub_corridor__floor=self.floor).first(); ac.turned_on = False; ac.save()

        payload = {
            "sub_corridor": SubCorridor.objects.filter(floor=self.floor).first().id
        }
        # create motion
        self.client.post('/api/trigger_motion/', data=payload, content_type='application/json')

        TriggerActions.motion_detection_trigger()

        # assert Light.objects.filter(sub_corridor__floor=floor).first().turned_on == True
        # assert AirConditioner.objects.filter(sub_corridor__floor=floor).first().turned_on == False

        sleep(3)

        TriggerActions.motion_detection_trigger()

        assert Light.objects.filter(sub_corridor__floor=self.floor).first().turned_on==False
        assert AirConditioner.objects.filter(sub_corridor__floor=self.floor).first().turned_on==False

