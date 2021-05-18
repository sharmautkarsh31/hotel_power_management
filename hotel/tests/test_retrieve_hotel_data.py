from django.test import TestCase

from hotel.models import Hotel


class TestRetrieveDataHotelAPI(TestCase):

    def setUp(self) -> None:
        self.url = '/api/hotel/'
        self.hotel_name = 'Test Hotel'
        self.floors = 2
        self.sub_corridors_per_floor = 2
        self.main_corridors_per_floor = 1
        self.create_hotel_data()
        self.hotel_id = Hotel.objects.get(name=self.hotel_name).id

    def create_hotel_data(self):
        payload = {
            "hotel_name": self.hotel_name,
            "floors": self.floors,
            "main_corridors": self.main_corridors_per_floor,
            "sub_corridors": self.sub_corridors_per_floor
        }
        self.client.post(self.url, data=payload, content_type='application/json')


    def test_retrieve_data(self):
        url = self.url + str(self.hotel_id) + '/'
        response = self.client.get(url)
        assert response.status_code == 200
        assert response.data["hotel_name"] == "Test Hotel"


    def test_invalid_hotel_id(self):
        url = self.url + 'invalid_id/'
        response = self.client.get(url)
        assert response.status_code == 404
        self.assertJSONEqual(response.content,{"detail":"Not found."})
