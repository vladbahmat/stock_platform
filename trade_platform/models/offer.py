from django.db import models

from trade_platform.models.item import Item
from trade_platform.models.profile import Profile


class Offer(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="offer_person")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="offer_item")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_sell = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity},{self.price},{self.is_active},{self.is_sell}"