from django.db import models
from .Stock import Stock


class DailyStockQuote(models.Model):
    value = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    stock = models.ForeignKey(Stock, related_name='daily_quote')
