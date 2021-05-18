from rest_framework import mixins
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from hotel.models import Hotel, MotionDetection
from hotel.serializers import HotelApplianceSerializer, HotelArtefactCreateSerializer, MotionDetectionSerializer


class HotelApplianceStateAPIView(
                                    mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.ListModelMixin,
                                    GenericViewSet
                                 ):

    permission_classes = [AllowAny]
    serializer_class = HotelApplianceSerializer
    queryset = Hotel.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return HotelArtefactCreateSerializer
        else:
            return HotelApplianceSerializer

class TriggerMotionAPIView(GenericViewSet,mixins.CreateModelMixin):

    permission_classes = [AllowAny]
    serializer_class = MotionDetectionSerializer
    queryset = MotionDetection.objects.all()






