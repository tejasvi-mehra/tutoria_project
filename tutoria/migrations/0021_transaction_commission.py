# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 15:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0020_auto_20171110_2202'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='commission',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
