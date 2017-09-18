from django.db import models
from .TradingAccount import TradingAccount


class Trade(models.Model):
    ts = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField()
    account = models.ForeignKey(TradingAccount)
