from rest_framework import serializers

from trade_platform.models import Offer


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


class ChangePriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = '__all__'

    def update(self, instance, validated_data):
        instance.price = validated_data.get('price', instance.price)
        return instance