import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "map_activity.settings")
django.setup()

from activity.models import Marker, Activity
import random
from faker import Faker

fake = Faker()

# Geographic coordinates of the area
min_lat, max_lat = 47.75, 48.75  # latitude
min_lon, max_lon = 33.0, 35.5  # longitude

# Create a list of activities
activities = ['Non-Food Items (NFI)', 'Evacuation', 'Water Distribution', 'Bread']


# Coordinates for random markers
def generate_random_coordinates():
    return [round(random.uniform(min_lat, max_lat), 6), round(random.uniform(min_lon, max_lon), 6)]


# Function to add test markers
def add_test_markers():
    for _ in range(50):  # You can change the number of markers you want to create (50 in this case)
        activity_name = random.choice(activities)
        activity = Activity.objects.get(name=activity_name)
        quantity = random.randint(10, 100)
        date = fake.date_between(start_date='-1y', end_date='today')
        location = generate_random_coordinates()
        place = fake.city()

        Marker.objects.create(
            activity=activity,
            quantity=quantity,
            date=date,
            location=location,
            place=place
        )


if __name__ == "__main__":
    add_test_markers()
