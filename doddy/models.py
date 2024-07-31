from django.contrib.auth.models import AbstractUser
from django.db import models


class DoddyUser(AbstractUser):
    tg_id = models.CharField(max_length=100, unique=True, verbose_name="Telegram ID")
    first_name = models.CharField(max_length=100, verbose_name="First Name")
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Last Name")
    tg_username = models.CharField(max_length=100, blank=True, null=True, verbose_name="Username")
    language_code = models.CharField(max_length=10, blank=True, null=True, verbose_name="Language Code")
    balance = models.BigIntegerField(default=0, verbose_name="Berry Balance")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    def __str__(self):
        return f"{self.first_name} {self.last_name} (@{self.username})"

    class Meta:
        verbose_name = "Doddy User"
        verbose_name_plural = "Doddy Users"
