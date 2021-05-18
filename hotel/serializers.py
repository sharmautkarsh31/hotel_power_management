from django.conf import settings

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from hotel.models import Hotel, Floor, MainCorridor, SubCorridor, AirConditioner, Light, MotionDetection


class MainCorridorSerializer(serializers.ModelSerializer):
    main_corridor_name = serializers.CharField(source='name',read_only=True)
    light = serializers.SerializerMethodField()
    air_conditioner = serializers.SerializerMethodField()

    def get_light(self,obj):
        return "On" if obj.light_set.first().turned_on else "Off"

    def get_air_conditioner(self,obj):
        return "On" if obj.airconditioner_set.first().turned_on else "Off"

    class Meta:
        model = MainCorridor
        fields = ("main_corridor_name", "light", "air_conditioner")


class SubCorridorSerializer(serializers.ModelSerializer):
    sub_corridor_name = serializers.CharField(source='name',read_only=True)
    light = serializers.SerializerMethodField()
    air_conditioner = serializers.SerializerMethodField()

    def get_light(self,obj):
        return "On" if obj.light_set.first().turned_on else "Off"

    def get_air_conditioner(self,obj):
        return "On" if obj.airconditioner_set.first().turned_on else "Off"

    class Meta:
        model = SubCorridor
        fields = ("sub_corridor_name", "light", "air_conditioner")


class FloorSerializer(serializers.ModelSerializer):
    floor_name = serializers.CharField(source='name',read_only=True)
    main_corridor = serializers.SerializerMethodField()
    sub_corridor = serializers.SerializerMethodField()

    def get_main_corridor(self,obj):
        return MainCorridorSerializer(obj.maincorridor_set.all(), many=True).data

    def get_sub_corridor(self,obj):
        return SubCorridorSerializer(obj.subcorridor_set.all(), many=True).data

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

            for i in range(self.validated_data['floors']):

                # create floor
                floor = Floor.objects.create(hotel=hotel)

                # create sub_corridor
                for i in range(self.validated_data['sub_corridors']):
                    sub_corridor = SubCorridor.objects.create(floor=floor)
                    Light.objects.create(sub_corridor=sub_corridor)
                    AirConditioner.objects.create(sub_corridor=sub_corridor)

                # create main_corridors
                for i in range(self.validated_data['main_corridors']):
                    main_corridor = MainCorridor.objects.create(floor=floor)
                    Light.objects.create(main_corridor=main_corridor)
                    AirConditioner.objects.create(main_corridor=main_corridor)
        return hotel


class MotionDetectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MotionDetection
        fields = ("sub_corridor",)
