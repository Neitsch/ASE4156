# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-12 21:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0009_auto_20171011_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='investmentbucket',
            name='total',
            field=models.FloatField(default=1000.0),
            preserve_default=False,
        ),
    ]