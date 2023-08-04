from django.urls import path
from .views import MarkerListAPIView, home

urlpatterns = [
    path('api/markers/', MarkerListAPIView.as_view(), name='marker-list'),
    path('', home, name='home'),
]
