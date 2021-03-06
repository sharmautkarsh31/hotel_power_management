# Generated by Django 3.2.3 on 2021-05-17 02:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airconditioner',
            name='main_corridor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.maincorridor'),
        ),
        migrations.AlterField(
            model_name='airconditioner',
            name='sub_corridor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.subcorridor'),
        ),
        migrations.AlterField(
            model_name='light',
            name='main_corridor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.maincorridor'),
        ),
        migrations.AlterField(
            model_name='light',
            name='sub_corridor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hotel.subcorridor'),
        ),
    ]
