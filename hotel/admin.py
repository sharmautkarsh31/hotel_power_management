from django.contrib import admin

# Register your models here.
from hotel.models import Hotel, Floor, Corridor

admin.site.register(Hotel)
admin.site.register(Floor)
admin.site.register(Corridor)


