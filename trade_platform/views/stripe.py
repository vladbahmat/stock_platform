import stripe
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin

from rest_framework.response import Response


class StripeView(viewsets.GenericViewSet,
                 ListModelMixin):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    @action(detail=False, methods=['POST'], url_path='retrieve_charge')
    def retrieve_charge(self, request, *args, **kwargs):
        stripe_charge = stripe.Charge.retrieve(
            request.data['charge_id'],
            stripe_account='acct_1J0LoOBRfThoA9Kk'
        )

        return Response(stripe_charge)

    @action(detail=False, methods=['POST'], url_path='add_customer')
    def add_customer(self, request, *args, **kwargs):
        stripe_charge = stripe.Customer.create(**request.data)

        return Response(stripe_charge)

    @action(detail=False, methods=['POST'], url_path='add_charge')
    def add_charge(self, request, *args, **kwargs):
        stripe_charge = stripe.Charge.create(
            **request.data
        )

        return Response(stripe_charge)

    @action(detail=False, methods=['POST'], url_path='retrieve_customer')
    def retrieve_customer(self, request, *args, **kwargs):
        stripe_charge = stripe.Customer.retrieve(
            "cus_JdgpxuuprF25YS"
        )

        return Response(stripe_charge)