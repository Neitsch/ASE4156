"""This module is for loading historical data for stocks"""
from yahoo_historical import Fetcher
from django.db.models.signals import post_save
from django.dispatch import receiver
import arrow
from .models import Stock, DailyStockQuote


def create_new_stock(ticker, name):
    """
    Function simply creates a new stock
    """
    stock = Stock(name=name, ticker=ticker)
    stock.save()
    return stock


def fill_quote_history(stock):
    """
    Given a stock, it fills in the last 10 years of historical data
    """
    now = arrow.now()
    ten_back = now.replace(years=-10)
    now = get_date_array_for_fetcher(now)
    ten_back = get_date_array_for_fetcher(ten_back)
    fetcher = Fetcher(stock.ticker, ten_back, now)
    history = fetcher.getHistorical()
    objects = []
    for row in history.itertuples():
        value = getattr(row, "Close")
        date = getattr(row, "Date")
        objects.append(
            DailyStockQuote(value=value, date=date, stock=stock))
    DailyStockQuote.objects.bulk_create(objects, batch_size=500)


def data_ten_years_back_for_stock(request):
    """ Function that creates Stock object
        and loads data for it 10 years back
    """
    if request.method == "POST":
        body = request.POST
        name = body['name']
        ticker = body['ticker']
        create_new_stock(ticker, name)


def get_date_array_for_fetcher(arrow_date):
    """Function that formats arrow date to Yahoo Fetcher format """
    return [arrow_date.year, arrow_date.month, arrow_date.day]


@receiver(post_save, sender=Stock)
def create_stock(instance, created, **_):
    """
    Queries stock quotes when stock is created
    """
    if created:
        fill_quote_history(instance)
