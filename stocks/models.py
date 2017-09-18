from django.db import models


class Stock(models.Model):
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10)


class DailyStockQuote(models.Model):
    value = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    stock = models.ForeignKey(Stock, related_name='daily_quote')
