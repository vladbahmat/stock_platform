from django.db import models

from trade_platform.models.item import Item
from trade_platform.models.profile import Profile


class WatchList(models.Model):
    person = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='watchlist')
    item = models.ManyToManyField(Item, related_name='watchlists')

    def __str__(self):
        return f"{self.person.user}"