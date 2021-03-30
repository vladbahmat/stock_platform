from rest_framework import serializers

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
    class Meta:
        model = Item
        fields = '__all__'


    def validate(self, data):
        if data['name']=='Shrek' and data['code']=='SHREK':
            raise serializers.ValidationError("Sorry we can't register item with this name and code")
        return data


class UpdateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('code',)


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'


    def validate_quantity(self, value):
        if value>10:
            raise serializers.ValidationError("You can't sell more than 10 items one time.")
        return value


class UpdateOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('is_active', 'is_sell', 'price', 'quantity', 'item')
