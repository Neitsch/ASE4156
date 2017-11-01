"""
Models keeps track of all the persistent data around stocks
"""
from datetime import date as os_date
from django.db.models import Q
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MinValueValidator
from authentication.models import Profile


class Stock(models.Model):
    """
    Stock represents a single stock. For example GOOGL
    """
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(
            1,
            message="The name should not be empty."
        )],
    )
    ticker = models.CharField(
        max_length=10,
        unique=True,
        validators=[MinLengthValidator(
            1,
            message="The ticker should not be empty."
        )],
    )

    def latest_quote(self, date=None):
        """
        Returns the latest quote for the stock
        """
        quote_query = self.daily_quote
        if date is not None:
            quote_query = quote_query.filter(date__leq=date)
        quote_query = quote_query.order_by('-date')
        if quote_query:
            return quote_query[0]
        return None

    @staticmethod
    def find_stock(text, first=None):
        """
        Finds the stocks that contain >text<
        """
        query = Stock.objects.filter(name__icontains=text)
        if first:
            query = query[:first]
        return query

    def __str__(self):
        return "{}, {}, {}".format(self.id, self.name, self.ticker)


class DailyStockQuote(models.Model):
    """
    DailyStockQuote is one day in the performance of a stock,
    for example 2nd July GOOGL value is 281.31$
    """
    value = models.FloatField(
        validators=[MinValueValidator(
            0.0,
            message="Daily stock quote can not be negative"
        )]
    )
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
    name = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(
            1,
            message="The name should not be empty."
        )],
    )
    owner = models.ForeignKey(Profile, related_name='owned_bucket')
    public = models.BooleanField()
    available = models.FloatField(
        validators=[MinValueValidator(
            0.0,
            message="The available money can not be negative."
        )]
    )

    class Meta(object):
        unique_together = ('name', 'owner')

    @staticmethod
    def accessible_buckets(profile):
        """
        Finds all buckets that the user could view
        """
        return InvestmentBucket.objects.filter(Q(owner=profile) | Q(public=True))


class InvestmentBucketDescription(models.Model):
    """
    An investment bucket represents a collection of stocks to invest in
    """
    text = models.CharField(
        max_length=255,
        validators=[MinLengthValidator(
            3,
            message="The description should at least be 3 characters long."
        )]
    )
    bucket = models.ForeignKey(InvestmentBucket, related_name='description')
    is_good = models.BooleanField()

    class Meta(object):
        unique_together = ('text', 'bucket')


class InvestmentStockConfiguration(models.Model):
    """
    Represents the configuration of how much of a stock to invest for a bucket
    """
    quantity = models.FloatField(
        validators=[MinValueValidator(
            0.0,
            message="The quantity can not be negative."
        )]
    )
    stock = models.ForeignKey(Stock, related_name='bucket')
    bucket = models.ForeignKey(InvestmentBucket, related_name='stocks')
    start = models.DateField(default=os_date.today, blank=True)
    end = models.DateField(null=True, blank=True)


@receiver(pre_save)
def pre_save_any(sender, instance, *_args, **_kwargs):
    """
    Ensures that all constrains are met
    """
    if sender.__name__ == 'Session':
        return
    try:
        instance.full_clean()
    except ValidationError as ex:
        raise Exception(ex.messages[0])
