from django.contrib.auth.models import User
from django.db.models import Value, Count, IntegerField
from django.db.models.functions import Concat
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from trade_platform.models import Position, WorkShift
from trade_platform.serializers import  PositionSerializer, PositionIndexValueSerializer
from trade_platform.serializers import UserSerializer
from trade_platform.services import send_email_language_notification


class UserView(viewsets.GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer
    queryset = User.objects.all()

    @action(detail=False, methods=['POST'], url_path='register')
    def register_user(self, request):
        data = request.data
        serialized = UserSerializer(data=data)
        serialized.is_valid()
        serialized.save()

        return Response(serialized.data)
