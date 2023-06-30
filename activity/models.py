

from django.db import models


class Marker(models.Model):
    ACTIVITY_CHOICES = [
        ('Раздача хлеба', 'Раздача хлеба'),
        ('Раздача воды', 'Раздача воды'),
        ('Раздача еды', 'Раздача еды'),

    ]

    activity = models.CharField(max_length=50, choices=ACTIVITY_CHOICES)
    quantity = models.IntegerField()
    date = models.DateField()
    place = models.CharField(max_length=100)
    location = models.JSONField()  # Предполагается, что location - это список [широта, долгота]

    def __str__(self):
        return self.place
