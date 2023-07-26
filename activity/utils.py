from .models import Marker
import folium
import requests




def filter_markers(activity_filter=None, date_filter=None):
    # Берем все объекты Marker из базы данных
    markers = Marker.objects.all()

    # Если переданы фильтры, применяем их
    if activity_filter is not None:
        markers = markers.filter(activity=activity_filter)

    if date_filter is not None:
        markers = markers.filter(date=date_filter)

    return markers


def create_popup_content(marker_data):
    """
    Function to create the HTML content of the popup for a marker.
    """
    return f"""
        <style> .leaflet-popup-content-wrapper {{width:300px; }} </style>
        <table style="width:100%;">
            <tr><th colspan="2" style="text-align:center;">{marker_data['place']}</th></tr>
            <tr><td style="text-align:left;"><b>Activity:</b></td><td style="text-align:left;">{marker_data['activity']}</td></tr>
            <tr><td style="text-align:left;"><b>Quantity:</b></td><td style="text-align:left;">{marker_data['quantity']}</td></tr>
            <tr><td style="text-align:left;"><b>Date:</b></td><td style="text-align:left;">{marker_data['date']}</td></tr>
            <tr><td style="text-align:left;"><b>Place:</b></td><td style="text-align:left;">{marker_data['place']}</td></tr>
        </table>
        """


def add_geojson_layer(m, url, layer_name):
    # Загружаем GeoJSON данные
    raw_data = requests.get(url).json()

    # Оставляем только полигоны
    geojson_data = {
        'type': 'FeatureCollection',
        'features': [feature for feature in raw_data['features'] if feature['geometry']['type'] != 'Point']
    }

    # Добавляем данные на карту
    geojson_layer = folium.GeoJson(
        data=geojson_data,
        name=layer_name,
        style_function=lambda x: {
            'fillColor': x['properties']['fill'],
            'color': x['properties']['stroke'],
            'weight': x['properties']['stroke-width'],
            'fillOpacity': x['properties']['fill-opacity']
        }
    )

    geojson_layer.add_to(m)


def create_map(markers):
    m = folium.Map(location=[48.5, 35], zoom_start=10,
                   tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                   attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')

    activity_layers = {}

    # Создаем слой для каждого вида активности
    for activity in Marker.ACTIVITY_CHOICES:
        activity_layers[activity[0]] = folium.FeatureGroup(name=activity[0])
        m.add_child(activity_layers[activity[0]])

    # Добавляем маркеры на соответствующие слои
    for marker_data in markers.values():
        location = marker_data['location']
        activity = marker_data['activity']
        popup_content = create_popup_content(marker_data)

        # Используем разные иконки в зависимости от активности
        if activity == 'Bread Distribution':
            icon = folium.Icon(color='orange', icon="bread-slice", prefix='fa')
        elif activity == 'Water distribution':
            icon = folium.Icon(color='blue', icon="tint", prefix='fa')
        elif activity == 'Food Distribution':
            icon = folium.Icon(color='green', icon="utensils", prefix='fa')
        elif activity == 'Non-Food Items (NFI)':
            icon = folium.Icon(color='purple', icon="cube", prefix='fa')
        elif activity == 'Evacuation':
            icon = folium.Icon(color='darkred', icon="truck-fast", prefix='fa')
        elif activity == 'Restoration of a damaged home':
            icon = folium.Icon(color='green', icon="tools", prefix='fa')
        else:
            icon = folium.Icon(color='gray', icon="flag", prefix='fa')  # fallback icon

        folium.Marker(
            location=location,
            popup=popup_content,
            icon=icon
        ).add_to(activity_layers[activity])

    # Добавляем слой GeoJSON
    add_geojson_layer(m, 'https://deepstatemap.live/api/history/1687169321/geojson', 'My GeoJSON Layer')

    # Добавляем управление слоями в интерфейс карты
    folium.LayerControl().add_to(m)

    return m
