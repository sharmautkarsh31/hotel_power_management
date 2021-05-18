import json

from django.test import TestCase

# Create your tests here.
from hotel.models import Hotel


class TestCreateHotelAPI(TestCase):

    def setUp(self) -> None:
        self.url = '/api/hotel/'

    def test_create_hotel_artefacts(self):
        payload = {
                "hotel_name": "Test Hotel",
                "floors": "2",
                "main_corridors": "1",
                "sub_corridors": "2"
        }
        response = self.client.post(self.url, data=payload, content_type='application/json')
        assert response.status_code == 201
        assert Hotel.objects.first().name == payload['hotel_name']

    def test_invalid_floor(self):
        payload = {
            "hotel_name": "Test Hotel",
            "floors": "0",
            "main_corridors": "1",
            "sub_corridors": "2"
        }
        response = self.client.post(self.url, data=payload, content_type='application/json')
        assert response.status_code == 400
        self.assertJSONEqual(response.content,
                             {"floors":["Ensure this value is greater than or equal to 1."]})


