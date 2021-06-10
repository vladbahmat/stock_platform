from django.db.models import When, Value, Case
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated

from rest_framework.response import Response

from trade_platform.models import Offer
from trade_platform.serializers import OfferSerializer, UpdateOfferSerializer, ChangePriceSerializer


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