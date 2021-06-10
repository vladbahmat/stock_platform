from rest_framework import serializers


class WorkShiftSerrializer(serializers.Serializer):
    name = serializers.CharField(max_length=30, read_only=True)
    is_active = serializers.BooleanField()