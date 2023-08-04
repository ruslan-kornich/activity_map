from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Marker
from .serializers import MarkerSerializer


class MarkerListAPIView(APIView):
    def get(self, request, format=None):
        markers = Marker.objects.all()
        serializer = MarkerSerializer(markers, many=True)
        return Response(serializer.data)


def home(request):
    return render(request, 'activity/home.html')
