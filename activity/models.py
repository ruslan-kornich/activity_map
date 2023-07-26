

from django.db import models


class Marker(models.Model):
    ACTIVITY_CHOICES = [
        ('Bread Distribution', 'Bread Distribution'),
        ('Water distribution', 'Water distribution'),
        ('Food Distribution', 'Food Distribution'),
        ('Non-Food Items (NFI)', 'Non-Food Items (NFI)'),
        ('Evacuation', 'Evacuation'),
        ('Restoration of a damaged home', 'Restoration of a damaged home')


    ]

    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    quantity = models.IntegerField()
    date = models.DateField()
    place = models.CharField(max_length=100)
    location = models.JSONField()  # It is assumed that location is a list of [latitude, longitude]

    def __str__(self):
        return self.place
