from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)
