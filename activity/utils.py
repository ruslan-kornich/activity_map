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

def create_map(markers, template='leaflet'):
    m = folium.Map(location=[48.5, 35], zoom_start=10,
                   tiles='https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png',
                   attr='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors')

    # Словарь для хранения групп маркеров по типу деятельности
    activity_groups = {}

    for marker_data in markers.values():
        location = marker_data['location']
        activity = marker_data['activity']
        quantity = marker_data['quantity']
        date = marker_data['date']
        place = marker_data['place']

        # Если группа для этой деятельности еще не создана, создаем ее
        if activity not in activity_groups:
            activity_groups[activity] = FeatureGroup(name=activity)
            m.add_child(activity_groups[activity])

        # Теперь добавляем маркер в соответствующую группу
        folium.Marker(
            location=location,
            popup="""
            <style> .leaflet-popup-content-wrapper {{width:300px; }} </style>
            <table style="width:100%;">
                <tr><th colspan="2" style="text-align:center;">{}</th></tr>
                <tr><td style="text-align:left;"><b>Activity:</b></td><td style="text-align:left;">{}</td></tr>
                <tr><td style="text-align:left;"><b>Quantity:</b></td><td style="text-align:left;">{}</td></tr>
                <tr><td style="text-align:left;"><b>Date:</b></td><td style="text-align:left;">{}</td></tr>
                <tr><td style="text-align:left;"><b>Place:</b></td><td style="text-align:left;">{}</td></tr>
            </table>
            """.format(place, activity, quantity, date, place),
            icon=folium.Icon(color='blue', icon="flag", prefix='fa')
        ).add_to(activity_groups[activity])

    LayerControl().add_to(m)  # добавляем элемент управления слоями

    return m





