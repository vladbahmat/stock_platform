from django.db import models
from django.utils import timezone

from trade_platform.models.location import Location
from trade_platform.models.managers.position_manager import PositionFullnameManager, APIManager, IndexValueManager
from trade_platform.models.workshift import WorkShift


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

    def __str__(self):
        return str(self.id)