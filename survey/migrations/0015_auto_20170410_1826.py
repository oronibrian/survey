# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-10 18:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0014_auto_20170410_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='response',
            name='user_uuid',
            field=models.IntegerField(default=1, editable=False),
        ),
        migrations.AlterField(
            model_name='mail',
            name='date_of_birth',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 10, 18, 26, 4, 338966)),
        ),
        migrations.AlterField(
            model_name='mail',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 10, 18, 26, 4, 339050)),
        ),
        migrations.AlterField(
            model_name='mail',
            name='start_date',
            field=models.DateField(blank=True, default=datetime.datetime(2017, 4, 10, 18, 26, 4, 339013)),
        ),
        migrations.AlterField(
            model_name='mail',
            name='user_uuid',
            field=models.IntegerField(default=267, editable=False),
        ),
        migrations.AlterField(
            model_name='survey',
            name='enddate',
            field=models.DateTimeField(default=datetime.datetime(2017, 5, 10, 18, 26, 4, 328184)),
        ),
    ]
