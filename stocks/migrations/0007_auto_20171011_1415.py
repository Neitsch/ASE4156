# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-11 14:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0006_auto_20171011_1412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='investmentbucket',
            name='invest_desc',
        ),
        migrations.AddField(
            model_name='investmentbucketdescription',
            name='bucket',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='description', to='stocks.InvestmentBucket'),
            preserve_default=False,
        ),
    ]
