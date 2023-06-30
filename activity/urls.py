from django.urls import path
from .views import home, create_point
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home, name='home'),
    path('create_point/', create_point, name='create_point'),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
