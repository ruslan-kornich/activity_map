from django.urls import path
from .views import (
    MarkerListAPIView,
    ActivityListAPIView,
    ActivitiesForPlaceView,
    home,
)

urlpatterns = [
    path(
        "api/markers/", MarkerListAPIView.as_view(), name="marker-list-all"
    ),  # Для получения всех маркеров
    path("api/activities/", ActivityListAPIView.as_view(), name="activ-list"),
    path(
        "api/activities_for_place/<str:place_name>/<str:activity_name>/",
        ActivitiesForPlaceView.as_view(),
    ),
    path("", home, name="home"),
]
