from django.db import models
from .TradingAccount import TradingAccount
from .Stock import Stock


class Trade(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    account = models.ForeignKey(TradingAccount, related_name='trades')
    stock = models.ForeignKey(Stock, related_name='trades')
