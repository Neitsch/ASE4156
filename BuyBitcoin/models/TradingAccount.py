from django.db import models
from django.contrib.auth.models import User


class TradingAccount(models.Model):
    account_name = models.CharField(max_length=30)
    user = models.ForeignKey(User, related_name='trading_accounts')
