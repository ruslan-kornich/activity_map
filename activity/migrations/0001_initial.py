# Generated by Django 4.2.2 on 2023-06-29 20:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('activity', models.CharField(choices=[('Раздача хлеба', 'Раздача хлеба'), ('Раздача воды', 'Раздача воды'), ('Раздача еды', 'Раздача еды')], max_length=50)),
                ('quantity', models.IntegerField()),
                ('date', models.DateField()),
                ('place', models.CharField(max_length=100)),
                ('location', models.JSONField()),
            ],
        ),
    ]
