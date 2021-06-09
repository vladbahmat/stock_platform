from django.db import models

from trade_platform.models.currency import Currency


class Item(models.Model):
    name = models.CharField("Name", max_length=15)
    code = models.CharField("Code", max_length=5, unique=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="item_currency")
    description = models.CharField("Description", max_length=100, default=' ')

    def __str__(self):
        return f"{self.code}"