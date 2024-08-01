from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from decimal import Decimal


class DoddyUser(AbstractUser):
    tg_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Last Name")
    tg_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    language_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Language Code")
    balance = models.BigIntegerField(default=0, verbose_name="Berry Balance")

    points_per_click = models.PositiveIntegerField(default=100, verbose_name="Berries per click")

    last_energy = models.PositiveIntegerField(default=1000, verbose_name="Last Energy")
    energy_last_updated = models.DateTimeField(default=timezone.now, verbose_name="Energy Last Updated")
    energy_recover_per_sec = models.DecimalField(
        max_digits=20,  # Total number of digits
        decimal_places=1,  # Number of decimal places
        default=Decimal('1.0'),
        verbose_name="Energy recover per sec"
    )
    max_energy = models.PositiveIntegerField(default=1000, verbose_name="Max Energy")

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
        new_energy = self.last_energy + recovered_energy

        if new_energy > self.max_energy:
            new_energy = self.max_energy

        return new_energy

    def update_energy(self, user_timestamp, clicks):
        now = timezone.now()
        if user_timestamp > now:
            print('Нас разводят1')
            return
        seconds_before_user = (user_timestamp - self.energy_last_updated).total_seconds()
        energy_accumulation = seconds_before_user * float(self.energy_recover_per_sec)

        energy_was = min(energy_accumulation + self.last_energy, self.max_energy)

        elapsed_time = (now - user_timestamp).total_seconds()
        energy_accum1 = elapsed_time * float(self.energy_recover_per_sec)

        if energy_was + energy_accum1 < clicks:
            print('Нас разводят')
            return
        else:
            self.last_energy = min(energy_was + energy_accum1 - clicks, self.max_energy)

        self.energy_last_updated = now
        self.save()

        return 'ok'

    class Meta:
        verbose_name = "Doddy User"
        verbose_name_plural = "Doddy Users"
