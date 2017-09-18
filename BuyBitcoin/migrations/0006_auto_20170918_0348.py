# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 03:48
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuyBitcoin', '0005_auto_20170918_0141'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stock',
            name='trade',
        ),
        migrations.AddField(
            model_name='trade',
            name='stock',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='stock_for_trade', to='BuyBitcoin.Stock'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dailystockquote',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stock_for_daily', to='BuyBitcoin.Stock'),
        ),
        migrations.AlterField(
            model_name='trade',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='account', to='BuyBitcoin.TradingAccount'),
        ),
        migrations.AlterField(
            model_name='tradingaccount',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
    ]
