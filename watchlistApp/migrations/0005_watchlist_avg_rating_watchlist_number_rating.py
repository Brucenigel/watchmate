# Generated by Django 4.2.5 on 2023-10-09 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlistApp', '0004_review_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
    ]