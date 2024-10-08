# Generated by Django 5.0.7 on 2024-08-01 16:51

import django.utils.timezone
from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doddy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="doddyuser",
            name="energy_last_updated",
            field=models.DateTimeField(
                default=django.utils.timezone.now, verbose_name="Energy Last Updated"
            ),
        ),
        migrations.AddField(
            model_name="doddyuser",
            name="energy_recover_per_sec",
            field=models.DecimalField(
                decimal_places=1,
                default=Decimal("1.0"),
                max_digits=20,
                verbose_name="Energy recover per sec",
            ),
        ),
        migrations.AddField(
            model_name="doddyuser",
            name="last_energy",
            field=models.PositiveIntegerField(default=1000, verbose_name="Last Energy"),
        ),
        migrations.AddField(
            model_name="doddyuser",
            name="max_energy",
            field=models.PositiveIntegerField(default=1000, verbose_name="Max Energy"),
        ),
        migrations.AddField(
            model_name="doddyuser",
            name="points_per_click",
            field=models.PositiveIntegerField(
                default=100, verbose_name="Berries per click"
            ),
        ),
    ]
