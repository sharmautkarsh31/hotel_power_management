# Generated by Django 3.2.3 on 2021-05-17 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0003_motiondetection'),
    ]

    operations = [
        migrations.RenameField(
            model_name='motiondetection',
            old_name='timestamp',
            new_name='motion_timestamp',
        ),
        migrations.AddField(
            model_name='motiondetection',
            name='action_timestamp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
