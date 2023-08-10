from django.urls import path
from .views import (
    MarkerListAPIView,
    ActivityListAPIView,
    ActivitySpecificMarkersAPIView,
    home,
)

urlpatterns = [
    path(
        "api/markers/", MarkerListAPIView.as_view(), name="marker-list-all"
    ),  # Для получения всех маркеров
    path(
        "api/markers/<str:activity>/",
        ActivitySpecificMarkersAPIView.as_view(),
        name="marker-list",
    ),  # Для получения маркеров определенной активности
    path("api/activities/", ActivityListAPIView.as_view(), name="activ-list"),
    path("", home, name="home"),
]
