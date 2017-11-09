"""
Tests the models of the Trading app
"""
from unittest import mock
import pytest
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from stocks.models import InvestmentBucket, Stock
from stocks.historical import create_stock
from yahoo_historical import Fetcher


def setup_module(module):
    """
    Mock out any externals
    """
    post_save.disconnect(receiver=create_stock, sender=Stock)
    module.original_init_method = Fetcher.__init__
    module.original_getHistorical_method = Fetcher.getHistorical
    Fetcher.__init__ = mock.Mock(return_value=None)
    Fetcher.getHistorical = mock.Mock(return_value=None)


def teardown_module(module):
    """
    Restore externals
    """
    Fetcher.__init__ = module.original_init_method
    Fetcher.getHistorical = module.original_getHistorical_method


@pytest.mark.django_db(transaction=True)
def test_trading_account_avail_buckets():
    """
    Test available buckets
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    buff = InvestmentBucket(name="buffet", owner=user.profile, public=False, available=1)
    buff.save()
    assert trading_account.available_buckets(buff) == 0
    trading_account.trade_bucket(buff, 1)
    assert trading_account.available_buckets(buff) == 1
    trading_account.trade_bucket(buff, 2342342342342234)
    assert trading_account.available_buckets(buff) == 2342342342342235
    trading_account.trade_bucket(buff, -2342342342342234)
    assert trading_account.available_buckets(buff) == 1
    trading_account.trade_bucket(buff, -1)
    assert trading_account.available_buckets(buff) == 0


@pytest.mark.django_db(transaction=True)
def test_trading_account_available_stock():
    """
    Test available stocks
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    stock = Stock(name="sto", ticker="sto")
    stock.save()
    quote = stock.daily_quote.create(
        value=4,
        date="2016-06-05"
    )
    assert trading_account.available_stocks(stock) == 0
    trading_account.trade_stock(stock, 1)
    assert trading_account.available_stocks(stock) == 1
    trading_account.trade_stock(stock, 2342342342342234)
    assert trading_account.available_stocks(stock) == 2342342342342235
    trading_account.trade_stock(stock, -2342342342342234)
    assert trading_account.available_stocks(stock) == 1
    trading_account.trade_stock(stock, -1)
    assert trading_account.available_stocks(stock) == 0


@pytest.mark.django_db(transaction=True)
def test_has_enough_bucket():
    """
    Test has enough bucket
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
        )
    buff = InvestmentBucket(name="buffet", owner=user.profile, public=False, available=1)
    buff.save()
    assert trading_account.has_enough_bucket(buff, 1) is False
    trading_account.trade_bucket(buff, 1)
    assert trading_account.has_enough_bucket(buff, 1)
    assert trading_account.has_enough_bucket(buff, 2) is False
    trading_account.trade_bucket(buff, 2342342342342234)
    assert trading_account.has_enough_buckets(buff, 2342342342342235)
    assert trading_account.has_enough_bucket(buff, 2342342342342236) is False
    trading_account.trade_bucket(buff, -2342342342342234)
    assert trading_account.has_enough_bucket(buff, 1)
    assert trading_account.has_enough_bucket(buff, 2) is False
    trading_account.trade_bucket(buff, -1)
    assert trading_account.has_enough_bucket(buff, 1) is False


@pytest.mark.django_db(transaction=True)
def test_has_enough_stock():
    """
    Test has enough stock
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    stock = Stock(name="sto", ticker="sto")
    stock.save()
    quote = stock.daily_quote.create(
        value=4,
        date="2016-06-05"
    )
    assert trading_account.has_enough_stock(stock, 1) is False
    trading_account.trade_stock(stock, 1)
    assert trading_account.has_enough_stock(stock, 1)
    assert trading_account.has_enough_stock(stock, 2) is False
    trading_account.trade_stock(stock, 2342342342342234)
    assert trading_account.enough_stock(stock, 2342342342342235)
    assert trading_account.has_enough_stock(stock, 2342342342342236) is False
    trading_account.trade_stock(stock, -2342342342342234)
    assert trading_account.has_enough_stock(stock, 1)
    assert trading_account.has_enough_stock(stock, 2) is False
    trading_account.trade_stock(stock, -1)
    assert trading_account.has_enough_stock(stock, 1) is False


@pytest.mark.django_db(transaction=True)
def test_trading_account_trade_bucket():
    """
    Test trade bucket
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    buffa = InvestmentBucket(name="buffeta", owner=user.profile, public=False, available=1)
    buffa.save()
    with pytest.raises(Exception):
        trading_account.trade_bucket(buffa, -2)
    trading_account.trade_bucket(buffa, 2)
    with pytest.raises(Exception):
        trading_account.trade_bucket(buffa, -3)
    assert trading_account.has_enough_bucket(buffa, 2)
    trading_account.trade_bucket(buffa, -2)
    assert trading_account.available_buckets(buffa) == 0


@pytest.mark.django_db(transaction=True)
def test_trading_account_trade_stock():
    """
    Test trade stock
    """
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    stock = Stock(name="sto", ticker='sto')
    stock.save()
    quote = stock.daily_quote.create(
        value=4,
        date="2016-06-05"
    )
    with pytest.raises(Exception):
        trading_account.trade_stock(stock, -2)
    trading_account.trade_stock(stock, 2)
    with pytest.raises(Exception):
        trading_account.trade_stock(stock, -3)
    assert trading_account.has_enough_stock(stock, 2)
    trading_account.trade_stock(stock, -2)
    assert trading_account.available_stocks(stock) == 0
