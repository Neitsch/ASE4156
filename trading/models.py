"""
Models here represents any interaction between a user and stocks
"""
from authentication.models import Profile
from django.db import models
from stocks.models import Stock


class TradingAccount(models.Model):
    """
    A TradingAccount is owned by a user, we associate stock trades with it.
    """
    account_name = models.CharField(max_length=30)
    profile = models.ForeignKey(Profile, related_name='trading_accounts')

    class Meta(object):
        unique_together = ('profile', 'account_name')


class Trade(models.Model):
    """
    A Trade represents a single exchange of a stock for money
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    account = models.ForeignKey(TradingAccount, related_name='trades')
    stock = models.ForeignKey(Stock, related_name='trades')
