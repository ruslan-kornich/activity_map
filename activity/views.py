from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Marker, Activity
from .serializers import MarkerSerializer, ActivitySerializer


class MarkerListAPIView(APIView):
    def get(self, request, format=None):
        markers = Marker.objects.all()
        serializer = MarkerSerializer(markers, many=True)
        # Получаем данные из связанных моделей Activity
        activity_ids = [marker['activity'] for marker in serializer.data]
        activities = Activity.objects.filter(id__in=activity_ids)
        activity_serializer = ActivitySerializer(activities, many=True)
        activity_data = {activity['id']: activity for activity in activity_serializer.data}
        # Добавляем данные из связанных моделей в ответ
        for marker_data in serializer.data:
            activity_id = marker_data['activity']
            marker_data['activity'] = activity_data.get(activity_id, {})
        return Response(serializer.data)


def home(request):
    return render(request, 'activity/home.html')