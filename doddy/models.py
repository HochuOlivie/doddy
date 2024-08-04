from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models import F, Sum
from django.utils import timezone
from decimal import Decimal
from math import floor


class DoddyUser(AbstractUser):
    tg_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Last Name")
    tg_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    language_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Language Code")
    balance = models.PositiveBigIntegerField(default=0, verbose_name="Berry Balance")

    points_per_click = models.PositiveIntegerField(default=100, verbose_name="Berries per click")

    last_energy = models.FloatField(default=1000, verbose_name="Last Energy")
    energy_last_updated = models.DateTimeField(default=timezone.now, verbose_name="Energy Last Updated")
    energy_recover_per_sec = models.DecimalField(
        max_digits=20,  # Total number of digits
        decimal_places=1,  # Number of decimal places
        default=Decimal('1.0'),
        verbose_name="Energy recover per sec"
    )
    max_energy = models.PositiveIntegerField(default=1000, verbose_name="Max Energy")

    bbc_balance = models.BigIntegerField(default=0, verbose_name="BBC Balance")

    last_farm_datetime = models.DateTimeField(default=timezone.now, verbose_name="Energy Last Updated")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"

    @property
    def current_energy(self):
        # Calculate the time elapsed since the last update
        now = timezone.now()
        elapsed_time = (now - self.energy_last_updated).total_seconds()

        # Calculate the recovered energy since the last update
        recovered_energy = elapsed_time * float(self.energy_recover_per_sec)

        # Calculate the new current energy
        new_energy = floor(min(self.last_energy + recovered_energy, self.max_energy))

        if new_energy > self.max_energy:
            new_energy = self.max_energy

        return floor(new_energy)

    def update_farm_per_sec_lock(self):
        with transaction.atomic():
            now = timezone.now()
            u = DoddyUser.objects.select_for_update().get(pk=self.pk)
            u.balance += floor((now - self.last_farm_datetime).total_seconds()) * self.berries_per_sec
            u.last_farm_datetime = now
            u.save()

    def update_farm_per_sec_no_lock(self):
        with transaction.atomic():
            now = timezone.now()
            self.balance += floor((now - self.last_farm_datetime).total_seconds()) * self.berries_per_sec
            self.last_farm_datetime = now
            self.save()

    @property
    def farm_berries(self):
        now = timezone.now()
        seconds = floor((now - self.last_farm_datetime).total_seconds())
        return seconds * self.berries_per_sec

    @property
    def total_balance(self):
        return self.balance + self.farm_berries

    @property
    def berries_per_sec(self):
        return self.farms.select_related('farm_type').annotate(
            income=F('farm_type__farm_per_sec') * F('level')
        ).aggregate(
            total_income=Sum('income')
        )['total_income'] or 0

    def update_energy(self, user_timestamp, clicks):
        now = timezone.now()

        if user_timestamp - timedelta(seconds=3) > now:
            print('Нас разводят1')
            return

        if user_timestamp > now:
            user_timestamp = now

        seconds_before_user = (user_timestamp - self.energy_last_updated).total_seconds()
        energy_accumulation = seconds_before_user * float(self.energy_recover_per_sec)

        energy_was = min(energy_accumulation + self.last_energy, self.max_energy)

        elapsed_time = (now - user_timestamp).total_seconds()
        energy_accum1 = elapsed_time * float(self.energy_recover_per_sec)

        if energy_was + energy_accum1 < clicks:
            print('Нас разводят')
            return
        else:
            le = min(energy_was + energy_accum1 - clicks, self.max_energy)
            print(le)
            if le < 0:
                print('Нас разводят')
                return
            self.last_energy = le
        self.energy_last_updated = now
        self.save()

        return 'ok'

    class Meta:
        verbose_name = "Doddy User"
        verbose_name_plural = "Doddy Users"


class Auction(models.Model):
    nft_number = models.PositiveIntegerField(default=0, verbose_name="Number of nfts in auction")
    date = models.DateTimeField(default=timezone.now(), verbose_name="Date")


class AuctionBet(models.Model):
    user = models.ForeignKey(DoddyUser, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    _berries = models.PositiveBigIntegerField(verbose_name="Berry Bet")
    min_bet = models.PositiveBigIntegerField(verbose_name="Min Bet")
    max_bet = models.PositiveBigIntegerField(verbose_name="Max Bet")

    @property
    def berries(self):
        return self._berries

    @berries.setter
    def berries(self, value):
        if value <= 0:
            raise ValueError('Berry Bets must be greater than 0')
        self.berries = value


class FarmType(models.Model):
    name = models.CharField(max_length=100, verbose_name="Farm Name")
    farm_per_sec = models.PositiveIntegerField(verbose_name="Farm per sec")
    cost_to_upgrade = models.PositiveBigIntegerField(verbose_name="Cost to Upgrade")


class UserFarm(models.Model):
    user = models.ForeignKey(DoddyUser, on_delete=models.CASCADE, related_name='farms')
    farm_type = models.ForeignKey(FarmType, on_delete=models.CASCADE)
    level = models.PositiveSmallIntegerField(verbose_name="Farm Level")


