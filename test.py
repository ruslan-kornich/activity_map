import os
import django
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "map_activity.settings")
django.setup()

from activity.models import Marker
import random
from faker import Faker

fake = Faker()

# Geographic coordinates of the area
city_lat, city_lon = 48.0, 34.0  # Coordinates of the city
activity = 'Bread Distribution'
min_date = fake.date_between(start_date='-1y', end_date='today')  # Random start date within the last year

for i in range(10):
    # Add days to the start date to create different dates
    date = min_date + timedelta(days=i)

    # Create markers with the same city, activity, and different dates
    Marker.objects.create(
        location=[city_lat, city_lon],
        activity=activity,
        quantity=random.randint(10, 100),
        date=date,
        place=fake.city()
    )
