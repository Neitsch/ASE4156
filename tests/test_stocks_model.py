import datetime
import pytest
from stocks.models import Stock


@pytest.mark.django_db(transaction=True)
def test_stock_latest_quote():
    stock = Stock(
        name="Name1",
        ticker="TKRC"
    )
    stock.save()
    correct_quote3 = stock.daily_quote.create(
        value=3,
        date="2016-06-03"
    )
    correct_quote1 = stock.daily_quote.create(
        value=4,
        date="2016-06-05"
    )
    correct_quote2 = stock.daily_quote.create(
        value=5,
        date="2016-06-06"
    )
    assert stock.latest_quote("2016-06-05") == correct_quote1
    assert stock.latest_quote() == correct_quote2
    assert stock.latest_quote("2016-06-04") == correct_quote3
    with pytest.raises(Exception):
        stock.latest_quote("2016-06-02")
    with pytest.raises(Exception):
        stock.latest_quote(datetime.datetime.now() + datetime.timedelta(days=3))
