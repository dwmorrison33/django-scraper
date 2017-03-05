# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 15:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ScrapeData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('permit_number', models.CharField(max_length=255)),
                ('status', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=555)),
                ('contractor', models.CharField(max_length=1255)),
                ('description', models.CharField(max_length=1555)),
                ('valuation', models.CharField(max_length=255)),
                ('licensed_professional', models.CharField(max_length=1255)),
                ('parcel_number', models.CharField(max_length=5255)),
                ('date_created', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
