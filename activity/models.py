from django.db import models

# models.py

ACTIVITY_ICONS = {
    'Bread Distribution': 'fa-bread-slice',
    'Water distribution': 'fa-tint',
    'Food Distribution': 'fa-utensils',
    'Non-Food Items (NFI)': 'fa-shopping-bag',
    'Evacuation': 'fa-hiking',
    'Restoration of a damaged home': 'fa-hammer',
}

ACTIVITY_COLORS = {
    'Bread Distribution': 'red',
    'Water distribution': 'blue',
    'Food Distribution': 'green',
    'Non-Food Items (NFI)': 'purple',
    'Evacuation': 'orange',
    'Restoration of a damaged home': 'darkred',
}

from django.db import models


class Activity(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=50, default='fa-bread-slice')
    color = models.CharField(max_length=50, default='orange')

    def __str__(self):
        return self.name


class Marker(models.Model):
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date = models.DateField()
    place = models.CharField(max_length=100)
    location = models.JSONField()

    def __str__(self):
        return self.place
