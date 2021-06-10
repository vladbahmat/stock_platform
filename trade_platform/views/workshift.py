import datetime

from django.db.models import Case, When, Value, BooleanField, F, Prefetch, Count, Q
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from trade_platform.models import Position, WorkShift
from trade_platform.serializers import WorkShiftSerrializer


class WorkShiftView(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = WorkShiftSerrializer
    queryset = Position.objects.all()

    @action(detail=False, methods=['get'], url_path='workshift_status')
    def get_workshift_status(self, request):
        queryset = WorkShift.objects.annotate(
            inversed_value=Case(
                When(is_active=True, then=Value(False)),
                default=Value(True),
                output_field=BooleanField()
            )
        ).update(is_active=F('inversed_value'))

        queryset = WorkShift.objects.all()
        serialized = WorkShiftSerrializer(queryset, many=True)
        return Response(serialized.data)

    @action(detail=False, methods=['get'], url_path='workshift1')
    def get_workshifts1(self, request):
        queryset = WorkShift.objects.all()
        serialized = WorkShiftSerrializer(queryset, many=True)
        return Response(serialized.data)

    @action(detail=False, methods=['get'], url_path='workshift2')
    def get_workshifts2(self, request):
        positions_queryset = Position.objects.all()
        queryset = WorkShift.objects.prefetch_related(Prefetch('positions', queryset=positions_queryset,to_attr='workshifts_positions'))
        print(queryset[0].workshifts_positions)
        serialized = WorkShiftSerrializer(queryset, many=True)
        return Response(queryset.values('id'))

    @action(detail=False, methods=['get'], url_path='workshift_date')
    def get_workshifts_by_date(self, request):
        queryset = WorkShift.objects.annotate(
            count_positions=Count('positions',
                                  filter= Q(starttime__date__gte=datetime.datetime.now()))
                                             ).values('id','count_positions')
        return Response(queryset)