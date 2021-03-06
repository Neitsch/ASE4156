# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-02 12:26
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import stocks.stock_helper


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0019_auto_20171030_2116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='ticker',
            field=models.CharField(max_length=10, unique=True, validators=[django.core.validators.MinLengthValidator(1, message='The ticker should not be empty.'), stocks.stock_helper.validate_ticker]),
        ),
    ]
