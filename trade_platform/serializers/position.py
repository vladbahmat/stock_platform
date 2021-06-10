from rest_framework import serializers

from trade_platform.models import Position


class PositionIndexValueSerializer(serializers.ModelSerializer):
    index_value = serializers.IntegerField()
    class Meta:
        model = Position
        fields = ('id', 'index_value')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'first_name')