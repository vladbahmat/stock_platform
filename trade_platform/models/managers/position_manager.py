import datetime

from django.db import models

from django.db.models import Count, QuerySet, IntegerField, Case, When
from django.db.models.functions import Cast
from django.db.models.functions import ExtractIsoYear, ExtractMonth
from django.contrib.postgres.aggregates import ArrayAgg

class NoDeleteExeption(Exception):
    def __init__(self, message='test exception'):
        self.message = message
        super().__init__(self, message)


class NoDeleteQuerySet(QuerySet):

    def delete(self):
        raise NoDeleteExeption()


class PositionFullnameManager(models.Manager):

    def get_queryset(self):
        query = NoDeleteQuerySet(self.model, using=self._db)

        return query


class APIManager(models.Manager):
    def get_queryset(self):
        return super(APIManager, self).get_queryset().annotate(workshifts_count=Count('workshifts'),
                                                               position_workshifts=ArrayAgg('workshifts'))


class IndexValueManager(models.Manager):
    def get_queryset(self):

        return super(IndexValueManager, self).get_queryset().annotate(
            index_value=Case(
                When(
                    contract_end_date__gte=datetime.date.today(),
                    then=Cast('location__factor', IntegerField()) * ExtractIsoYear('contract_start_date')),
                When(contract_end_date__lt=datetime.date.today(),
                    then=Cast('location__factor', IntegerField()) * ExtractMonth('contract_start_date')),
                output_field=IntegerField())
        )