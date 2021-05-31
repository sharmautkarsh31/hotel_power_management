from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.timezone import now

from hotel.utils.helpers import generic_save_model_name


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


class Corridor(models.Model):
    name = models.CharField(max_length=255, unique=True)
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class MainCorridor(Corridor):

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class SubCorridor(Corridor):

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Appliance(models.Model):
    name = models.CharField(max_length=255, unique=True)
    turned_on = models.BooleanField(default=True)
    main_corridor = models.ForeignKey(MainCorridor, models.CASCADE, null=True, blank=True)
    sub_corridor = models.ForeignKey(SubCorridor, models.CASCADE, null=True, blank=True)

    class Meta:
        abstract = True


class Light(Appliance):
    power_consumption_unit = 5

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class AirConditioner(Appliance):
    power_consumption_unit = 10

    def save(self, *args, **kwargs):
        self = generic_save_model_name(self)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class MotionDetection(models.Model):
    motion_timestamp = models.DateTimeField(default=now)
    sub_corridor = models.ForeignKey(SubCorridor, models.CASCADE, null=True, blank=True)
    action_taken = models.BooleanField(default=False)

    def __str__(self):
        return (self.sub_corridor.name + self.motion_timestamp.strftime('%B %d %Y %H:%M:%S'))



