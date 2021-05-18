# Generated by Django 3.2.3 on 2021-05-18 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0005_auto_20210517_1441'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='motiondetection',
            name='action_1_taken',
        ),
        migrations.RemoveField(
            model_name='motiondetection',
            name='action_2_taken',
        ),
        migrations.AddField(
            model_name='motiondetection',
            name='action_taken',
            field=models.BooleanField(default=False),
        ),
    ]