import pytest
from django.contrib.auth.models import User
from stocks.models import InvestmentBucket, Stock

# @pytest.mark.django_db(transaction=True)
# def test_trading_account_total_value():
#     user = User.objects.create(username='christophe', password="iscool")
#     trading_account = user.profile.trading_accounts.create(
#         account_name="spesh"
#     )
"""Total value is currently not defined"""
""" Have to write an available cash test, after fixing
available cash (current implementation is incorrect) """


@pytest.mark.django_db(transaction=True)
def test_trading_account_available_buckets():
	"""
	Test available buckets
	"""
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    buff = InvestmentBucket(name="buffet", owner=user.profile, public=False, available=1).save()
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
    stock = Stock(name="sto", ticker="sto").save()
    assert trading_account.available_stock(stock) == 0
    trading_account.trade_stock(stock, 1)
    assert trading_account.available_stock(stock) == 1
    trading_account.trade_stock(stock, 2342342342342234)
    assert trading_account.available_stock(stock) == 2342342342342235
    trading_account.trade_stock(stock, -2342342342342234)
    assert trading_account.available_stock(stock) == 1
    trading_account.trade_stock(stock, -1)
    assert trading_account.available_stock(stock) == 0


""" Have to write a has enough cash test, after fixing
available cash (current implementation is incorrect) """


@pytest.mark.django_db(transaction=True)
def test_has_enough_bucket():
	"""
	Test has enough bucket
	"""
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
        )
    buff = InvestmentBucket(name="buffet", owner=user.profile, public=False, available=1).save()
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
    stock = Stock(name="sto", ticker="sto").save()
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
    buffa = InvestmentBucket(name="buffeta", owner=user.profile, public=False, available=1).save()
    with pytest.raises(Exception):
        trading_account.trade_bucket(buffa, -2)
    trading_account.trade_bucket(buffa, 2)
    with pytest.raises(Exception):
        trading_account.trade_bucket(buffa, -3)
    assert trading_account.has_enough_bucket(buffa, 2)
    trading_account.trade_bucket(buffa, -2)
    assert trading_account.available_bucket(buffa) == 0


@pytest.mark.django_db(transaction=True)
def test_trading_account_trade_stock():
	"""
	Test trade stock
	"""
    user = User.objects.create(username='christophe', password="iscool")
    trading_account = user.profile.trading_accounts.create(
        account_name="spesh"
    )
    stock = Stock(name="sto", ticker='sto').save()
    with pytest.raises(Exception):
        trading_account.trade_stock(stock, -2)
    trading_account.trade_stock(stock, 2)
    with pytest.raises(Exception):
        trading_account.trade_stock(stock, -3)
    assert trading_account.has_enough_stock(stock, 2)
    trading_account.trade_stock(stock, -2)
    assert trading_account.available_stock(stock) == 0
