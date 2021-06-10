from rest_framework import viewsets, status
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import  AllowAny

from rest_framework.response import Response

from trade_platform.models import Item
from trade_platform.serializers import ItemSerializer, UpdateItemSerializer, DetailItemSerializer
from trade_platform.tasks import send_item_update_notificate


class ItemView(viewsets.GenericViewSet,
               ListModelMixin,
               UpdateModelMixin,
               RetrieveModelMixin,
               CreateModelMixin):
    permission_classes = (AllowAny,)
    queryset = Item.objects.all()
    http_method_names = ('get', 'post', 'patch')
    serializer_classes_by_action = {
        'list': ItemSerializer,
        'retrieve': DetailItemSerializer,
        'update': UpdateItemSerializer,
        'create': DetailItemSerializer,
    }

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        send_item_update_notificate.apply_async([instance.id])
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response("Incorrect request",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, ItemSerializer)