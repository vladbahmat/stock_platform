from django.db import models
from django.utils import timezone

from trade_platform.models.workshift_plan import WorkShiftPlan


class WorkShift(models.Model):
    is_active = models.BooleanField(default=True)
    name = models.CharField(max_length=16)
    starttime = models.DateTimeField(default=timezone.now)
    endtime = models.DateTimeField(default=timezone.now)
    workshit_plan = models.ForeignKey(WorkShiftPlan, blank=True, null=True, on_delete=models.SET_NULL, related_name="workshifts")