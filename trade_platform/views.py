import time
import datetime
from django.db import connection
from django.db.models import When, Case, Value, IntegerField, BooleanField, F
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.decorators import action
from django.db.models.functions import Concat
from django.db.models import Value, Count, Q, Prefetch
from django.contrib.postgres.aggregates import ArrayAgg, JSONBAgg
from trade_platform.serializers import (ItemSerializer, OfferSerializer, InventorySerializer,
    UpdateItemSerializer, UpdateOfferSerializer, DetailItemSerializer, DetailWatchListSerializer,
    WatchListSerializer, ChangePriceSerializer, WorkShiftSerrializer, PositionSerializer,PositionIndexValueSerializer)
from trade_platform.models import Inventory, Item, WatchList, Offer, WorkShift, Position
from trade_platform.tasks import change_price, send_item_update_notificate
from trade_platform.services import send_email_language_notification
from django.utils import translation
from django.utils.translation import ugettext_lazy as _

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
                                  filter=Q(starttime__date__gte=datetime.datetime.now()))
                                             ).values('id','count_positions')
        return Response(queryset)


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
        #queryset = self.get_queryset()
        # serialized = PositionSerializer(position)
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


class InventoryView(viewsets.GenericViewSet,
                    ListModelMixin):
    permission_classes = (AllowAny,)
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()

    def list(self, request, *args, **kwargs):
        a = WorkShift.objects.all().prefetch_related('positions')#тут получаю все объекты воркшифта
        #print(a[0].positionss) #дальше надо по каждому из них пройти и достать оттуда лист позициЙ
        #print(a)
        #print(len(connection.queries))
        serializer = WorkShiftSerrializer(a, many=True)
        b = WorkShift.objects.annotate(workshift_positions=ArrayAgg('positions')).values('name', 'workshift_positions', 'starttime')
        #print(serializer.data)
        #print(len(connection.queries))
        # queryset = self.get_queryset().filter(person__user=1)
        # serializer = self.serializer_class(queryset, many=True)
        return Response(b)


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

    @action(detail=False, methods=['get'], url_path='my_watchlist')
    def my_watchlist(self, request, *args, **kwargs):
        queryset = request.user.profile.watchlist
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)


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
    #3 items 30ms

    @action(detail=False, methods=['post'], url_path='change_price_ser')
    def change_price_ser(self, request):
        for offer in Offer.objects.filter(pk__in=request.data['offers']):
            ChangePriceSerializer(data=offer.__dict__).update(offer, request.data).save()
        return Response("Changed successfully")
    #3 items 500+ms

    @action(detail=False, methods=['post'], url_path='change_price_task')
    def change_price_task(self, request):
        info = request.data
        offers = []
        prices = []
        for elem in info:
            offers.append(elem['offer'])
            prices.append(elem['price'])
        #good_offers = Offer.objects.filter(pk__in=offers)
        for  new_price in prices:
            Offer.objects.update(price=Case(
                When(pk__in=offers, then=Value(new_price))))
        print(Offer.objects.all())
        #Offer.objects.bulk_update(good_offers, ['price'])
        # Offer.objects.update(offer_id = Case(
        #     When(pk_in = [offers], then=Value()
        # ))
        return Response("Changed successfully")
    #3 items 12ms
