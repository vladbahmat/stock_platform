import time

from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import action

from trade_platform.serializers import ItemSerializer, OfferSerializer, InventorySerializer, \
    UpdateItemSerializer, UpdateOfferSerializer, DetailItemSerializer, DetailWatchListSerializer, \
    WatchListSerializer, ChangePriceSerializer
from trade_platform.models import Inventory, Item, WatchList, Offer
from trade_platform.tasks import change_price


class InventoryView(viewsets.GenericViewSet,
                    ListModelMixin):
    permission_classes = (IsAuthenticated,)
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(person__user=request.user)
        serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data)


class WatchListView(viewsets.GenericViewSet,
                    ListModelMixin,
                    UpdateModelMixin,
                    RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = WatchList.objects.all()
    http_method_names = ('get', 'patch')
    serializer_classes_by_action = {
        'list': WatchListSerializer,
        'retrieve': DetailWatchListSerializer,
        'update': WatchListSerializer,
    }

    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response("Incorrect request",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, WatchListSerializer)

    def list(self, request, *args, **kwargs):
        queryset = request.user.profile.watchlist
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


class ItemView(viewsets.GenericViewSet,
               ListModelMixin,
               UpdateModelMixin,
               RetrieveModelMixin,
               CreateModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Item.objects.all()
    http_method_names = ('get', 'post', 'patch')
    serializer_classes_by_action = {
        'list': ItemSerializer,
        'retrieve': DetailItemSerializer,
        'partial_update': UpdateItemSerializer,
        'create': DetailItemSerializer,
    }


    def http_method_not_allowed(self, request, *args, **kwargs):
        return Response("Incorrect request",
                        status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, ItemSerializer)


class OfferView(viewsets.GenericViewSet,
                ListModelMixin,
                CreateModelMixin,
                UpdateModelMixin,
                RetrieveModelMixin):
    permission_classes = (IsAuthenticated,)
    queryset = Offer.objects.all()
    serializer_classes_by_action = {
        'list': OfferSerializer,
        'retrieve': OfferSerializer,
        'partial_update': UpdateOfferSerializer,
        'create': OfferSerializer,
    }

    def create(self, request, *args, **kwargs):
        data = {**request.data, 'person': request.user.profile.id}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        return self.serializer_classes_by_action.get(self.action, OfferSerializer)


    @action(detail=False, methods=['post'], url_path='change_price')
    def change_price(self, request):
        Offer.objects.filter(pk__in=request.data['offers']).update(price=request.data['price'])
        return Response("Changed successfully")

    @action(detail=False, methods=['post'], url_path='change_price_ser')
    def change_price_ser(self, request):
        for offer in Offer.objects.filter(pk__in=request.data['offers']):
            ChangePriceSerializer(data=offer.__dict__).update(offer, request.data).save()
        return Response("Changed successfully")

    @action(detail=False, methods=['post'], url_path='change_price_task')
    def change_price_task(self, request):
        info = request
        change_price.s(info)
        return Response("Changed successfully")
