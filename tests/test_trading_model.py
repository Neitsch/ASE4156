import random
import string
import pytest
from trading.models import TradingAccount
from django.contrib.auth.models import User
from trading.models import TradeStock
from stocks.models import Stock
from stocks.historical import create_stock
from django.db.models.signals import post_save
from yahoo_historical import Fetcher
from unittest import mock


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
def test_trading_available_cash():
    """
    Testing available_cash for a Trading Account
    """
    pwd = ''.join(random.choices(string.ascii_uppercase + string.digits, k=9))
    user = User.objects.create(username='user', password=pwd)
    account = TradingAccount(profile=user.profile, account_name="testAccount")
    account.save()

    value_of_stock1 = 3
    stock1 = Stock.create_new_stock(
        name="Name1X",
        ticker="TKRC"
    )
    stock1.daily_quote.create(
        value=value_of_stock1,
        date="2016-06-03"
    )

    value_of_stock2 = 4
    quantity2 = 3
    stock2 = Stock.create_new_stock(
        name="Name2X",
        ticker="TKF"
    )
    stock2.daily_quote.create(
        value=value_of_stock2,
        date="2016-06-03"
    )
    TradeStock(quantity=1, account=account, stock=stock1).save()

    value = account.available_cash()
    assert value == -value_of_stock1

    TradeStock(quantity=quantity2, account=account, stock=stock2).save()
    value = account.available_cash()
    assert value == -value_of_stock1 + -value_of_stock2 * quantity2
