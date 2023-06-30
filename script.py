from  activity.models import Marker
import random
from faker import Faker

fake = Faker()

# Географические координаты района
min_lat, max_lat = 47.75, 48.75 # широта
min_lon, max_lon = 33.0, 35.5  # долгота

for _ in range(10):
    lat = random.uniform(min_lat, max_lat)
    lon = random.uniform(min_lon, max_lon)
    Marker.objects.create(
        location=[float(lat), float(lon)], # преобразование в float
        activity='Раздача хлеба',
        quantity=random.randint(10, 100),
        date=fake.date_between(start_date='-1y', end_date='today'),
        place=fake.city()
    )

