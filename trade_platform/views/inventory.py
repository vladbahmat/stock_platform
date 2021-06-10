from django.contrib.postgres.aggregates import ArrayAgg
from rest_framework import viewsets
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import AllowAny

from rest_framework.response import Response

from trade_platform.models import Inventory, WorkShift
from trade_platform.serializers import InventorySerializer, WorkShiftSerrializer


class InventoryView(viewsets.GenericViewSet,
                    ListModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def list(self, request, *args, **kwargs):
        a = WorkShift.objects.all().prefetch_related('positions')
        serializer = WorkShiftSerrializer(a, many=True)
        b = WorkShift.objects.annotate(workshift_positions=ArrayAgg('positions')).values('name', 'workshift_positions', 'starttime')
        return Response(b)