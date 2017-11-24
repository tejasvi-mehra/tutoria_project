# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 16:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0041_merge_20171123_1850'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='expire',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='forReview',
            field=models.BooleanField(default=False),
        ),
    ]
