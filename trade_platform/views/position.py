import datetime

from django.db.models import Value, Count, IntegerField
from django.db.models.functions import Concat
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from trade_platform.models import Position, WorkShift
from trade_platform.serializers import  PositionSerializer, PositionIndexValueSerializer
from trade_platform.services import send_email_language_notification


class PositionView(viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = PositionSerializer
    queryset = Position.objects.all()

    @action(detail=False, methods=['get'], url_path='positions1')
    def get_positions_1(self, request):
        queryset = self.get_queryset()
        serialized = PositionSerializer(queryset, many=True)

        return Response(serialized.data)

    @action(detail=False, methods=['get'], url_path='positions2')
    def get_positions_2(self, request):
        send_email_language_notification(request.user.email, request.user.config.language_code)
        queryset = Position.index_value_manager.all()
        serialized = PositionIndexValueSerializer(queryset, many=True)
        return Response(serialized.data)

    @action(detail=False, methods=['patch'], url_path='positions3/(?P<pk>\d+)')
    def get_positions_3(self, request, pk=None):
        position = Position.objects.get(id=pk)
        position.first_name = request.data['first_name']
        position.save()
        position.workshifts.add(WorkShift.objects.first())
        return Response({'first_name':position.workshifts})

    @action(detail=False, methods=['get'], url_path='positions4')
    def get_positions_4(self, request):
        data = Position.objects.all()
        serialized = PositionSerializer(data)
        return Response(serialized.data)

    @action(detail=False, methods=['get'], url_path='positions5')
    def get_positions_5(self, request):
        data = Position.objects.annotate(
            full_name=Concat('first_name', Value(' '), 'last_name'),
            workhsifts_count=Count('workshifts', output_field=IntegerField())
        ).values('id','full_name',  'workhsifts_count')
        return Response(data)