from django.contrib.auth.models import User
from django.db import models

from trade_platform.models.currency import Currency


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(decimal_places=5, max_digits=20, null=True, blank=True, default=5000)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL, related_name="currency")

    def __str__(self):
        return f"{self.user}"