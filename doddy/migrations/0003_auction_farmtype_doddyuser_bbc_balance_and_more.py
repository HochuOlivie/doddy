# Generated by Django 5.0.7 on 2024-08-03 18:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("doddy", "0002_doddyuser_energy_last_updated_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Auction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nft_number",
                    models.PositiveIntegerField(
                        default=0, verbose_name="Number of nfts in auction"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FarmType",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, verbose_name="Farm Name")),
                (
                    "farm_per_sec",
                    models.PositiveIntegerField(verbose_name="Farm per sec"),
                ),
            ],
        ),
        migrations.AddField(
            model_name="doddyuser",
            name="bbc_balance",
            field=models.BigIntegerField(default=0, verbose_name="BBC Balance"),
        ),
        migrations.AlterField(
            model_name="doddyuser",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=100, null=True, verbose_name="First Name"
            ),
        ),
        migrations.CreateModel(
            name="AuctionBet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("_berries", models.PositiveBigIntegerField(verbose_name="Berry Bet")),
                ("min_bet", models.PositiveBigIntegerField(verbose_name="Min Bet")),
                ("max_bet", models.PositiveBigIntegerField(verbose_name="Max Bet")),
                (
                    "auction",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doddy.auction"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserFarm",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("level", models.PositiveSmallIntegerField(verbose_name="Farm Level")),
                (
                    "farm_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="doddy.farmtype"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="farms",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
