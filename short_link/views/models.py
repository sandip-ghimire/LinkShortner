from django.db import models
from django.utils import timezone


class Urls(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    short_url = models.CharField(max_length=50)
    long_url = models.CharField(max_length=100)
    created_date = models.DateTimeField(default=timezone.now)
    click_count = models.IntegerField(default=0)
    click_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.long_url
