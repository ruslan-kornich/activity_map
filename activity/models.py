from django.contrib.gis.db import models

ACTIVITY_ICONS = {
    "Bread Distribution": "fa-bread-slice",
    "Water distribution": "fa-tint",
    "Food Distribution": "fa-utensils",
    "Non-Food Items (NFI)": "bag-shopping",
    "Evacuation": "truck-fast",
    "Restoration of a damaged home": "fa-hammer",
    "Hygiene": "hands-bubbles",
}

ACTIVITY_COLORS = {
    "Bread Distribution": "red",
    "Water distribution": "blue",
    "Food Distribution": "green",
    "Non-Food Items (NFI)": "purple",
    "Evacuation": "orange",
    "Restoration of a damaged home": "darkred",
    "Hygiene": "gray",
}


class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(
        max_length=50,
        choices=[(icon, icon) for icon in ACTIVITY_ICONS.values()],
        default="fa-bread-slice",
    )
    color = models.CharField(
        max_length=50,
        choices=[(color, color) for color in ACTIVITY_COLORS.values()],
        default="orange",
    )

    def __str__(self):
        return self.name


class Marker(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    beneficiary = models.IntegerField()
    date = models.DateField()
    place = models.CharField(max_length=100)
    location = models.PointField()  # Using PointField to store geographical data

    def __str__(self):
        return self.place
