import json
from time import sleep

import requests
from django.utils import timezone

from hotel.models import Hotel

base_url = 'http://localhost:8000'


def get_hotel_obj():
    print("\n\nHotel List:-")
    hotels = Hotel.objects.all().values('id', 'name', )
    for index, hotel in enumerate(hotels):
        print(index + 1, ". ", hotel['name'])

    hotel_index = int(input("Please enter the hotel index you want to monitor: ")) - 1
    hotel_name = str(hotels[hotel_index]['name'])
    hotel = Hotel.objects.get(name=hotel_name)
    return hotel


def print_response(response):
    print("\n\n\n", timezone.now().strftime('%B %d %Y %H:%M:%S'))
    response_data = json.loads(response.content)
    for floor in response_data['floor']:
        print(floor['floor_name'])
        print("    Main Corridors:-")
        for main_corridor in floor['main_corridor']:
            print("        ", main_corridor['name'], "--> Light: ", main_corridor['light'], ", AC: ",
                  main_corridor['air_conditioner'], "\n")
            print("    Sub Corridors:-")
            for sub_corridor in floor['sub_corridor']:
                print("        ", sub_corridor['name'], "--> Light: ", sub_corridor['light'], ", AC: ",
                      sub_corridor['air_conditioner'], "\n")

def main():
    hotel = get_hotel_obj()
    while True:
        response = requests.get(base_url + '/api/hotel/{}/'.format(hotel.id))
        if response.status_code == 200:
            print_response(response)
        else:
            print("status_code: ", response.status_code)
            print("response_data: ", response.content)
            break
        sleep(10)


def run():
    print("####### HOTEL APPLIANCES LIVE MONITOR ########")

    # while not settings.NIGHT_SHIFT_ACTIVE:
    #     print("Night mode not activated yet night mode will start at {}:{}----".format(
    #         settings.NIGHT_SHIFT_START['hour'], settings.NIGHT_SHIFT_START['minute']))
    #     sleep(1)
    # print("---- NIGHT MODE TURNED ON ----")
    main()



