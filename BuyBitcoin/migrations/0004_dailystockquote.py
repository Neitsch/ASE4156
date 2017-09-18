# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-18 01:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuyBitcoin', '0003_stock'),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyStockQuote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=16)),
                ('date', models.DateField()),
            ],
        ),
    ]
