from rest_framework.routers import SimpleRouter

from hotel.apis import HotelApplianceStateAPIView, TriggerMotionAPIView

router = SimpleRouter(trailing_slash=True)


router.register("hotel", HotelApplianceStateAPIView, basename='hotel')
router.register('trigger_motion', TriggerMotionAPIView, basename='trigger-motion')

