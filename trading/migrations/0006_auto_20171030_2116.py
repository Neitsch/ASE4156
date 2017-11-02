# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-30 21:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0019_auto_20171030_2116'),
        ('trading', '0005_auto_20171015_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='TradeBucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckettrades', to='trading.TradingAccount')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckettrades', to='stocks.InvestmentBucket')),
            ],
        ),
        migrations.RenameModel(
            old_name='Trade',
            new_name='TradeStock',
        ),
    ]
