# Generated by Django 3.2.3 on 2021-05-31 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0007_floorpowerconsumptionperhour'),
    ]

    operations = [
        migrations.AlterField(
            model_name='floorpowerconsumptionperhour',
            name='units_consumed',
            field=models.FloatField(default=0.0),
        ),
    ]
