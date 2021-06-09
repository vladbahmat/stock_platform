from django.db.models.signals import post_save, m2m_changed

from trade_platform.models import User, Profile, WatchList, Position, WorkShift


def create_profile(sender, **kwargs):
    if kwargs['created']:
        Profile.objects.create(user=kwargs['instance'])


def create_watchlist(sender, **kwargs):
    if kwargs['created']:
        WatchList.objects.create(person=kwargs['instance'])


def m2m_test_print(sender, **kwargs):
    #if kwargs['action']=='post_add':
    print("hello")

post_save.connect(create_profile, sender=User)
post_save.connect(create_watchlist, sender=Profile)
m2m_changed.connect(m2m_test_print, sender=Position.workshifts.through)
