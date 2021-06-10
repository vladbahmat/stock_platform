from rest_framework import serializers

from trade_platform.models import WatchList


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