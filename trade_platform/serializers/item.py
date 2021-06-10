from rest_framework import serializers

from trade_platform.models import Item


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