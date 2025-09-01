import datetime
from datetime import timezone

from django.db import models
from django.db.models import ForeignKey
from rest_framework.fields import IntegerField, CharField, ImageField


class Sensor(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True)


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name="measurements")
    temperature = models.FloatField(null=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    image = models.ImageField(null=True)
