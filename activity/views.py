from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Marker
from .utils import filter_markers, create_map

from django.contrib.auth.decorators import login_required
from decimal import Decimal


def home(request):
    # Получение параметров фильтров
    activity_filter = request.GET.get('activity')
    date_filter = request.GET.get('date')

    # Фильтрация маркеров
    filtered_markers = filter_markers(activity_filter, date_filter)

    # Создание карты с отфильтрованными маркерами
    map_object = create_map(filtered_markers)

    # Сохранение карты в HTML-строку
    map_html = map_object.get_root().render()

    return render(request, 'activity/home.html', {'map_html': map_html})


@csrf_exempt
@login_required
def create_point(request):
    if request.method == 'POST':
        lat = Decimal(request.POST.get('latitude'))
        lon = Decimal(request.POST.get('longitude'))
        comment = request.POST.get('comment')
        Marker.objects.create(user=request.user, latitude=lat, longitude=lon, comment=comment)
        return JsonResponse({'message': 'Success'}, status=201)
    return JsonResponse({'message': 'Bad request'}, status=400)
