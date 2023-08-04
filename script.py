import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "map_activity.settings")
django.setup()

from activity.models import Marker
import random
from faker import Faker

fake = Faker()

# Geographic coordinates of the area
min_lat, max_lat = 47.75, 48.75  # latitude
min_lon, max_lon = 33.0, 35.5  # longitude

# Coordinates for specific cities
cities = [
    {'name': 'Днепр', 'latitude': 48.4593, 'longitude': 35.0386},
    {'name': 'Запорожье', 'latitude': 47.8388, 'longitude': 35.1396},
    {'name': 'Харьков', 'latitude': 49.9935, 'longitude': 36.2304},
]

for city in cities:
    lat = city['latitude']
    lon = city['longitude']
    Marker.objects.create(
        location=[float(lat), float(lon)],
        activity='Water distribution',
        quantity=random.randint(10, 100),
        date=fake.date_between(start_date='-1y', end_date='today'),
        place=city['name']
    )
