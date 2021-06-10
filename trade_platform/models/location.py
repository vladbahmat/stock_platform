from django.db import models


class Location(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    factor = models.IntegerField(default=0)