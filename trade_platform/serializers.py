from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from trade_platform.models import Item, Inventory, WatchList, Offer


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
    # code = serializers.CharField(source="currency.code")
    # test = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = '__all__'

    # def get_test(self, obj):
    #     return obj.currency.code


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
