from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save



#м2м поле для вочлиста, для гет/поста запросов
# разное количество полей сделать!(вроде как разные сериалайзеры можно делать))




class Currency(models.Model):
    code = models.CharField("Code", max_length=5, unique=True)
    name = models.CharField("Name", max_length=15, unique=True, null=True)

    def __str__(self):
        return self.code


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    balance = models.DecimalField(decimal_places=5, max_digits=20, null=True, blank=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.user},{self.balance}"


# class Price(models.Model):
#     cost = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)
#
#     def __str__(self):
#         return f"{self.cost}"


class Item(models.Model):
    name = models.CharField("Name", max_length=15)
    code = models.CharField("Code", max_length=5, unique=True)
    currency = models.ForeignKey(Currency, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.CharField("Desc", max_length=100, default=' ')

    def __str__(self):
        return f"{self.code}"


class WatchList(models.Model):
    person = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='watchlist') #m2m
    item = models.ManyToManyField(Item, related_name='watchlists')

    def __str__(self):
        return f"{self.person.user}"


class Inventory(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity}"


class Offer(models.Model):
    person = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL)
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(decimal_places=5, max_digits=15, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_sell = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.person},{self.item},{self.quantity},{self.price},{self.is_active},{self.is_sell}"


class Trade(models.Model):
    item = models.ForeignKey(Item, blank=True, null=True, on_delete=models.SET_NULL)
    seller = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="seller_trade")
    buyer = models.ForeignKey(Profile, blank=True, null=True, on_delete=models.SET_NULL, related_name="buyer_trade")
    quantity = models.IntegerField()
    description = models.CharField("Desc", max_length=100)
    seller_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL,
                                     related_name="seller_offer")
    buyer_offer = models.ForeignKey(Offer, blank=True, null=True, on_delete=models.SET_NULL, related_name="buyer_offer")


