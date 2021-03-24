from django.contrib import admin
from trade_platform.models import *

myModels = [Profile, Currency, Trade, Offer, WatchList, Item, Inventory]
admin.site.register(myModels)
