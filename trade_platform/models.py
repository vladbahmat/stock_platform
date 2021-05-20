import datetime

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from trade_platform.manager import PositionFullnameManager, APIManager, IndexValueManager


class UserConfig(models.Model):
    LANGUAGE_CODE = [
        ('en', 'English'),
        ('ru', 'Russian'),
        ('ch', 'Chinese'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="config")
    language_code = models.CharField(max_length=2, choices=LANGUAGE_CODE, default='en')

class Location(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    factor = models.IntegerField(default=0)


class WorkShiftPlan(models.Model):
    name = models.CharField(max_length=30)
    startdate = models.DateField(default=timezone.now)
    enddate = models.DateField(default=timezone.now)


class WorkShift(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=16)
    starttime = models.DateTimeField(default=timezone.now)
    endtime = models.DateTimeField(default=timezone.now)
    workshit_plan = models.ForeignKey(WorkShiftPlan, blank=True, null=True, on_delete=models.SET_NULL, related_name="workshifts")


class Position(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    workshifts = models.ManyToManyField(WorkShift,related_name='positions')
    contract_start_date = models.DateField(default=timezone.now)
    contract_end_date = models.DateField(default=timezone.now)
    location = models.ForeignKey(Location, blank=True, null=True, on_delete=models.SET_NULL, related_name="position")

    objects = PositionFullnameManager()
    api_manager = APIManager()
    index_value_manager = IndexValueManager()
    # def delete(self, using=None, keep_parents=False):
    #     if self.api_manager:
    #         raise Exception
    #     else:
    #         raise Exception

    def __str__(self):
        return str(self.id)

class Currency(models.Model):
    code = models.CharField("Code", max_length=5, unique=True)
    name = models.CharField("Name", max_length=15, unique=True, null=True)

    def __str__(self):
        return self.code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(decimal_places=5, max_digits=20, null=True, blank=True, default=5000)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL, related_name="currency")

    def __str__(self):
        return f"{self.user}"


class Item(models.Model):
    name = models.CharField("Name", max_length=15)
    code = models.CharField("Code", max_length=5, unique=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL,
                                 related_name="item_currency")
    description = models.CharField("Description", max_length=100, default=' ')

    def __str__(self):
        return f"{self.code}"


class WatchList(models.Model):
    person = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='watchlist')
    item = models.ManyToManyField(Item, related_name='watchlists')

    def __str__(self):
        return f"{self.person.user}"


class Inventory(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL,
                               related_name="person_inventory")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="item_inventory")
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity}"


class Offer(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="offer_person")
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL, related_name="offer_item")
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_sell = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity},{self.price},{self.is_active},{self.is_sell}"


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


