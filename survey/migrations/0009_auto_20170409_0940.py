# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-09 09:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0008_auto_20170409_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mail',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 9, 9, 40, 50, 942469)),
        ),
        migrations.AlterField(
            model_name='mail',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 9, 9, 40, 50, 942545)),
        ),
        migrations.AlterField(
            model_name='mail',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 9, 9, 40, 50, 942513)),
        ),
        migrations.AlterField(
            model_name='survey',
            name='enddate',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 9, 9, 40, 50, 931825)),
        ),
    ]
