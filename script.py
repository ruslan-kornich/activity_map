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

for _ in range(10):
    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)
    Marker.objects.create(
        location=[float(lat), float(lon)],  # conversion to float
        activity='Restoration of a damaged home',
        quantity=random.randint(10, 100),
        date=fake.date_between(start_date='-1y', end_date='today'),
        place=fake.city()
    )
