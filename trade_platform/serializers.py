from rest_framework import serializers
from trade_platform.models import *


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('quantity', 'item')


class DetailWatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = '__all__'


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('item',)

    def update(self, instance, validated_data):
        instance.item.add(*validated_data.pop('item'))
        instance.save()

        return instance


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('name', 'code')


class DetailItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('code',)


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('is_active', 'is_sell', 'price', 'quantity', 'item')
