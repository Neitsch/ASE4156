from django.db import models
from django.contrib.auth.models import User
from stocks.models import Stock


class TradingAccount(models.Model):
    account_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name='trading_accounts')


class Trade(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    account = models.ForeignKey(TradingAccount, related_name='trades')
    stock = models.ForeignKey(Stock, related_name='trades')
