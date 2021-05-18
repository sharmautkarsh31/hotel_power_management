from django.contrib import admin

# Register your models here.
from hotel.models import Hotel, Floor, SubCorridor, MainCorridor, AirConditioner, Light

admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(SubCorridor)
admin.site.register(MainCorridor)
admin.site.register(AirConditioner)
admin.site.register(Light)

