"""This module is for loading historical data for stocks"""
from yahoo_historical import Fetcher

import arrow
from django.db.models import Max
from .models import Stock, DailyStockQuote


def data_ten_years_back_for_stock(request):
    """ Function that creates Stock object
        and loads data for it 10 years back
    """
    if request.method == "POST":
        body = request.POST
        name = body['name']
        ticker = body['ticker']
        stock = Stock(name=name, ticker=ticker)
        stock.save()
        now = arrow.now()
        ten_back = now.replace(years=-10)
        now = get_date_array_for_fetcher(now)
        ten_back = get_date_array_for_fetcher(ten_back)
        fetcher = Fetcher(ticker, ten_back, now)
        history = fetcher.getHistorical()
        save_stock_quote_from_fetcher(history, stock.id)


def get_date_array_for_fetcher(arrow_date):
    """Function that formats arrow date to Yahoo Fetcher format """
    return [arrow_date.year, arrow_date.month, arrow_date.day]


def fill_stocks(request):
    """Function that fills stock data for missing days"""
    if request.method == "POST":
        stock_id_field = 'stock_id'
        stock_ticker = 'stock__ticker'
        date = 'date'
        data = DailyStockQuote.objects.values(stock_ticker, stock_id_field).annotate(date=Max(date))
        for stock in data:
            last_date = arrow.get(stock[date]).replace(days=+1)
            last_date = get_date_array_for_fetcher(last_date)
            now = get_date_array_for_fetcher(arrow.now())
            ticker = stock[stock_ticker]
            stock_id = stock[stock_id_field]
            fetcher = Fetcher(ticker, last_date, now)
            history = fetcher.getHistorical()
            save_stock_quote_from_fetcher(history, stock_id)


def save_stock_quote_from_fetcher(fetcher_history, stock_id):
    """Function that saves DailyStockQuote from yahoo_historical fetcher"""
    objects = []
    for row in fetcher_history.itertuples():
        value = getattr(row, "Close")
        date = getattr(row, "Date")
        objects.append(
            DailyStockQuote(value=value, date=date, stock_id=stock_id))
    DailyStockQuote.objects.bulk_create(objects, batch_size=500)
