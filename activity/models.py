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
    location = models.JSONField()
    icon = models.CharField(max_length=50, choices=ACTIVITY_ICONS.items(), default='fa-bread-slice')
    color = models.CharField(max_length=50, choices=ACTIVITY_COLORS.items(), default='orange')

    def __str__(self):
        return self.place
