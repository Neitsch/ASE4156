"""
Models keeps track of all the persistent data around stocks
"""

from django.db import models


class Stock(models.Model):
    """
    Stock represents a single stock. For example GOOGL
    """
    name = models.CharField(max_length=255)
    ticker = models.CharField(max_length=10, unique=True)


class DailyStockQuote(models.Model):
    """
    DailyStockQuote is one day in the performance of a stock,
    for example 2nd July GOOGL value is 281.31$
    """
    value = models.DecimalField(max_digits=16, decimal_places=2)
    date = models.DateField()
    stock = models.ForeignKey(Stock, related_name='daily_quote')

    class Meta(object):
        """
        We use this to define our uniqueness constraint
        """
        unique_together = ('stock', 'date',)
