# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-22 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0033_merge_20171121_2308'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='tags',
            field=models.CharField(default='', max_length=10000),
        ),
    ]
