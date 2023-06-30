from typing import List

from .models import Marker
import folium


def filter_markers(activity_filter=None, date_filter=None):
    # Берем все объекты Marker из базы данных
    markers = Marker.objects.all()

    # Если переданы фильтры, применяем их
    if activity_filter is not None:
        markers = markers.filter(activity=activity_filter)

    if date_filter is not None:
        markers = markers.filter(date=date_filter)

    return markers


from folium import FeatureGroup, LayerControl


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
            icon = folium.Icon(color='blue', icon="bread-slice", prefix='fa')
        elif activity == 'Water distribution':
            icon = folium.Icon(color='green', icon="tint", prefix='fa')
        elif activity == 'Food Distribution':
            icon = folium.Icon(color='orange', icon="utensils", prefix='fa')
        else:
            icon = folium.Icon(color='gray', icon="flag", prefix='fa')  # fallback icon

        folium.Marker(
            location=location,
            popup=popup_content,
            icon=icon
        ).add_to(activity_layers[activity])

    # Добавляем управление слоями в интерфейс карты
    folium.LayerControl().add_to(m)
    return m






