"""
Tests the models of the Trading app
"""
import pytest
from stocks.models import InvestmentBucket
from django.contrib.auth.models import User


@pytest.mark.django_db(transaction=True)
def test_quick():
    user = User.objects.create(username='user1', password="a")
    bucket1 = InvestmentBucket(name='b1', public=False, available=1000, owner=user.profile)
    bucket2 = InvestmentBucket(name='b2', public=False, available=1000, owner=user.profile)
    bucket1.save()
    bucket2.save()
    acc = user.profile.trading_accounts.create(account_name="acc")
    assert acc.available_buckets(bucket1) == 0
    acc.buckettrades.create(quantity=2, stock=bucket1)
    assert acc.available_buckets(bucket1) == 2
    acc.buckettrades.create(quantity=4, stock=bucket1)
    assert acc.available_buckets(bucket2) == 0
    acc.buckettrades.create(quantity=3, stock=bucket2)
    assert acc.available_buckets(bucket1) == 6
    assert acc.available_buckets(bucket2) == 3
