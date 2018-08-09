# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-12-04 15:29
from __future__ import unicode_literals

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('trading', '0001_initial'), ('trading', '0002_auto_20170919_1336'), ('trading', '0003_auto_20170919_1456'), ('trading', '0004_auto_20170920_0123'), ('trading', '0005_auto_20171015_1523'), ('trading', '0006_auto_20171030_2116'), ('trading', '0007_auto_20171102_1226')]

    initial = True

    dependencies = [
        ('stocks', '0001_initial'),
        ('authentication', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('stocks', '0019_auto_20171030_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ts', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='TradingAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('account_name', models.CharField(max_length=30)),
                ('profile', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='trading_accounts', to='authentication.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='trade',
            name='account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='trading.TradingAccount'),
        ),
        migrations.AddField(
            model_name='trade',
            name='stock',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trades', to='stocks.Stock'),
        ),
        migrations.RenameField(
            model_name='trade',
            old_name='ts',
            new_name='timestamp',
        ),
        migrations.AlterUniqueTogether(
            name='tradingaccount',
            unique_together=set([('profile', 'account_name')]),
        ),
        migrations.AlterField(
            model_name='trade',
            name='quantity',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0, message='Daily stock quote can not be negative')]),
        ),
        migrations.CreateModel(
            name='TradeBucket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckettrades', to='trading.TradingAccount')),
                ('stock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buckettrades', to='stocks.InvestmentBucket')),
                ('quantity', models.FloatField(default=1)),
            ],
        ),
        migrations.RenameModel(
            old_name='Trade',
            new_name='TradeStock',
        ),
        migrations.AlterField(
            model_name='tradestock',
            name='quantity',
            field=models.FloatField(),
        ),
    ]
