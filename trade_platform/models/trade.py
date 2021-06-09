from django.db import models

from trade_platform.models.item import Item
from trade_platform.models.offer import Offer
from trade_platform.models.profile import Profile


class Trade(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item_trade")
    seller = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="seller_trade")
    buyer = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="buyer_trade")
    quantity = models.IntegerField()
    description = models.CharField("Desc", max_length=100)
    seller_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="seller_offer")
    buyer_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL, related_name="buyer_offer")

    def __str__(self):
        return f"{self.seller},{self.buyer},{self.quantity},{self.item}"