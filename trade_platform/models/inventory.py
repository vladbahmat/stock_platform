from django.db import models

from trade_platform.models.item import Item
from trade_platform.models.profile import Profile


class Inventory(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name="person_inventory")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item_inventory")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity}"