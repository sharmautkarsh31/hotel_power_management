from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from hotel.utils.helpers import generic_save_model_name, create_model_name


class Hotel(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Floor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    extreme_power_saver = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class FloorPowerConsumptionPerHour(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    hour_of_day = models.IntegerField(validators=[
            MaxValueValidator(23),
            MinValueValidator(0)
        ])
    units_consumed = models.FloatField(default=0.0)


class CorridorType(models.Model):
    type = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)


class Corridor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    corridor_type = models.ForeignKey(CorridorType, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        floor_id = str(Floor.objects.count())
        self.name = 'Floor'+ floor_id + ' ' + create_model_name(self,name=self.corridor_type.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class ApplianceType(models.Model):
    type = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    power_consumption_unit = models.IntegerField()


class Appliance(models.Model):
    name = models.CharField(max_length=255, unique=True)
    appliance_type = models.ForeignKey(ApplianceType, models.CASCADE, null=True, blank=True)
    turned_on = models.BooleanField(default=True)
    corridor = models.ForeignKey(Corridor, models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self,self.appliance_type.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MotionDetection(models.Model):
    motion_timestamp = models.DateTimeField(default=now)
    corridor = models.ForeignKey(Corridor, models.CASCADE, null=True, blank=True)
    action_taken = models.BooleanField(default=False)

    def __str__(self):
        return (self.corridor.name + self.motion_timestamp.strftime('%B %d %Y %H:%M:%S'))

