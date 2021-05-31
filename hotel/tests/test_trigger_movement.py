import random

from django.test import TestCase

from hotel.models import SubCorridor


class TestTriggerMotionAPI(TestCase):

    def setUp(self) -> None:
        self.url = '/api/trigger_motion/'
        self.hotel_name = 'Test Hotel'
        self.floors = 2
        self.sub_corridors_per_floor = 2
        self.main_corridors_per_floor = 1
        self.create_hotel_data()
        sub_corridors = SubCorridor.objects.all().values_list('id',flat=True)
        self.random_sub_corridor_id = random.choice(sub_corridors)

    def create_hotel_data(self):
        url = '/api/hotel/'
        payload = {
            "hotel_name": self.hotel_name,
            "floors": self.floors,
            "main_corridors": self.main_corridors_per_floor,
            "sub_corridors": self.sub_corridors_per_floor
        }
        self.client.post(url, data=payload, content_type='application/json')

    def test_motion_in_sub_corridor(self):
        payload = {
            "sub_corridor": self.random_sub_corridor_id
        }
        response = self.client.post(self.url, data=payload, content_type='application/json')
        assert response.status_code == 201

    def test_invalid_sub_corridor(self):
        payload = {
            "sub_corridor": "abc"
        }
        response = self.client.post(self.url, data=payload, content_type='application/json')
        assert response.status_code == 400
