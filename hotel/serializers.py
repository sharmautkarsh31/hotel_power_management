from django.conf import settings

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from hotel.models import Hotel, Floor, Corridor, MotionDetection, Appliance, ApplianceType, CorridorType


class CorridorSerializer(serializers.ModelSerializer):
    light = serializers.SerializerMethodField()
    air_conditioner = serializers.SerializerMethodField()

    def get_light(self,obj):
        light = obj.appliance_set.filter(appliance_type__type='LIGHT').first()
        if not light:
            return "No Light"
        return "On" if light.turned_on else "Off"

    def get_air_conditioner(self,obj):
        air_conditioner = obj.appliance_set.filter(appliance_type__type='AIR_CONDITIONER').first()
        if not air_conditioner:
            return "No AC"
        return "On" if air_conditioner.turned_on else "Off"

    class Meta:
        model = Corridor
        fields = ("name", "light", "air_conditioner")

#
# class SubCorridorSerializer(serializers.ModelSerializer):
#     sub_corridor_name = serializers.CharField(source='name',read_only=True)
#     light = serializers.SerializerMethodField()
#     air_conditioner = serializers.SerializerMethodField()
#
#     def get_light(self,obj):
#         light = obj.appliance_set.filter(appliance_type__type='LIGHT').first()
#         if not light:
#             return "No Light"
#         return "On" if light.turned_on else "Off"
#
#     def get_air_conditioner(self,obj):
#         air_conditioner = obj.appliance_set.filter(appliance_type__type='AIR_CONDITIONER').first()
#         if not air_conditioner:
#             return "No AC"
#         return "On" if air_conditioner.turned_on else "Off"
#
#     class Meta:
#         model = SubCorridor
#         fields = ("sub_corridor_name", "light", "air_conditioner")


class FloorSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='name',read_only=True)
    main_corridor = serializers.SerializerMethodField()
    sub_corridor = serializers.SerializerMethodField()

    def get_main_corridor(self,obj):
        return CorridorSerializer(obj.corridor_set.filter(corridor_type__type='MAIN_CORRIDOR'), many=True).data

    def get_sub_corridor(self,obj):
        return CorridorSerializer(obj.corridor_set.filter(corridor_type__type='SUB_CORRIDOR'), many=True).data

    class Meta:
        model = Floor
        fields = ("floor_name", "main_corridor", "sub_corridor",)


class HotelApplianceSerializer(serializers.ModelSerializer):
    hotel_name = serializers.CharField(source='name')
    floor = serializers.SerializerMethodField()

    def get_floor(self, obj):
        return FloorSerializer(obj.floor_set.all().order_by('-id'), many=True).data

    def get_current_time(self,obj):
        return timezone.now().strftime('%B %d %Y %H:%M:%S')

    def get_night_shift_active(self,obj):
        return settings.NIGHT_SHIFT_ACTIVE

    class Meta:
        model = Hotel
        fields = ("id","hotel_name","floor")


class HotelArtefactCreateSerializer(serializers.Serializer):
    hotel_name = serializers.CharField(required=True)
    floors = serializers.IntegerField(required=True, max_value=10,min_value=1)
    main_corridors = serializers.IntegerField(required=True,max_value=50,min_value=0)
    sub_corridors = serializers.IntegerField(required=True,max_value=50,min_value=0)

    def save(self, **kwargs):
        with transaction.atomic():
            #create Hotel
            hotel = Hotel.objects.create(name=self.validated_data['hotel_name'])

            light_type = ApplianceType.objects.get(type='LIGHT')
            air_conditioner_type = ApplianceType.objects.get(type='AIR_CONDITIONER')

            sub_corridor_type = CorridorType.objects.get(type='SUB_CORRIDOR')
            main_corridor_type = CorridorType.objects.get(type='MAIN_CORRIDOR')

            for i in range(self.validated_data['floors']):

                # create floor
                floor = Floor.objects.create(hotel=hotel)

                # create sub_corridor
                for i in range(self.validated_data['sub_corridors']):
                    sub_corridor = Corridor.objects.create(floor=floor,corridor_type=sub_corridor_type)
                    Appliance.objects.create(corridor=sub_corridor,appliance_type=light_type)
                    Appliance.objects.create(corridor=sub_corridor,appliance_type=air_conditioner_type)

                # create main_corridors
                for i in range(self.validated_data['main_corridors']):
                    main_corridor = Corridor.objects.create(floor=floor,corridor_type=main_corridor_type)
                    Appliance.objects.create(corridor=main_corridor,appliance_type=light_type)
                    Appliance.objects.create(corridor=main_corridor,appliance_type=air_conditioner_type)
        return hotel


class MotionDetectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MotionDetection
        fields = ("corridor",)
