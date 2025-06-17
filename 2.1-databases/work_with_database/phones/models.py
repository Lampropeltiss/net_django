from django.db import models


class Phone(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(null=True)
    image = models.CharField(null=True)
    release_date = models.DateField(null=True)
    lte_exists = models.BooleanField(null=True)
    slug = models.SlugField()
