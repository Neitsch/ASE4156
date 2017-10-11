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

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.name, self.ticker)


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

    def __str__(self):
        return "{}, {}, {}, {}".format(self.id,
                                       self.value,
                                       self.date,
                                       self.stock_id)


class InvestmentBucket(models.Model):
    """
    An investment bucket represents a collection of stocks to invest in
    """
    name = models.CharField(max_length=255)


class InvestmentBucketDescription(models.Model):
    """
    An investment bucket represents a collection of stocks to invest in
    """
    text = models.CharField(max_length=255)
    bucket = models.ForeignKey(InvestmentBucket, related_name='description')
    is_good = models.BooleanField()


class InvestmentStockConfiguration(models.Model):
    """
    Represents the configuration of how much of a stock to invest for a bucket
    """
    quantity = models.DecimalField(max_digits=8, decimal_places=2)
    stock = models.ForeignKey(Stock, related_name='bucket')
    bucket = models.ForeignKey(InvestmentBucket, related_name='stocks')
