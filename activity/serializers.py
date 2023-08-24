from rest_framework import serializers
from .models import Marker, Activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = "__all__"


class MarkerSerializer(serializers.ModelSerializer):
    activity = ActivitySerializer()
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = Marker
        fields = ("id", "activity", "quantity", "beneficiary", "date", "place", "lat", "lng")

    def get_lat(self, obj):
        return obj.location.y

    def get_lng(self, obj):
        return obj.location.x
