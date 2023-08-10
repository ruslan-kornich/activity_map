from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.gis.geos import Polygon

from .serializers import MarkerSerializer
from .models import Marker, Activity
from .serializers import ActivitySerializer


class MarkerListAPIView(APIView):
    def get(self, request, format=None):
        ne_lat = request.GET.get("maxLat")
        sw_lat = request.GET.get("minLat")
        ne_lng = request.GET.get("maxLng")
        sw_lng = request.GET.get("minLng")

        if not all([ne_lat, sw_lat, ne_lng, sw_lng]):
            # If no coordinates are provided, return all markers
            markers = Marker.objects.all().select_related("activity")
        else:
            try:
                ne_lat = float(ne_lat)
                sw_lat = float(sw_lat)
                ne_lng = float(ne_lng)
                sw_lng = float(sw_lng)

                # Create a polygon for the given area
                bbox = Polygon.from_bbox((sw_lng, sw_lat, ne_lng, ne_lat))

                # Get the markers that are inside the specified area
                markers = Marker.objects.filter(location__within=bbox).select_related(
                    "activity"
                )

            except ValueError:
                return Response(
                    {"error": "Invalid coordinates format"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data)


class ActivityListAPIView(APIView):
    def get(self, request, format=None):
        activities = Activity.objects.all()
        serializer = ActivitySerializer(activities, many=True)
        return Response(serializer.data)


class ActivitySpecificMarkersAPIView(APIView):
    def get(self, request, activity, format=None):
        try:
            activity_obj = Activity.objects.get(name=activity)
            markers = Marker.objects.filter(activity=activity_obj)
            serializer = MarkerSerializer(markers, many=True)

            for marker_data in serializer.data:
                marker_data["activity"] = ActivitySerializer(activity_obj).data

            return Response(serializer.data)
        except Activity.DoesNotExist:
            return Response(
                {"error": "Activity not found"}, status=status.HTTP_404_NOT_FOUND
            )


def home(request):
    return render(request, "activity/home.html")
