from django.db import models
from django.utils import timezone


class WorkShiftPlan(models.Model):
    name = models.CharField(max_length=30)
    startdate = models.DateField(default=timezone.now)
    enddate = models.DateField(default=timezone.now)
