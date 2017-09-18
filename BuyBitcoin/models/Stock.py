from django.db import models
from .Trade import Trade


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
    trade = models.ManyToManyField(Trade)
