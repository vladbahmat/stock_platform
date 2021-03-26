from django.db.models.signals import post_save
from django.dispatch import receiver
from trade_platform.models import User, Profile, WatchList


def create_profile(sender, **kwargs):
    if kwargs['created']:
        #print(kwargs['instance'].id)
        user_profile = Profile.objects.create(user=kwargs['instance'])


def create_watchlist(sender, **kwargs):
    if kwargs['created']:
        WatchList.objects.create(person=kwargs['instance'])


post_save.connect(create_profile, sender=User)
post_save.connect(create_watchlist, sender=Profile)



