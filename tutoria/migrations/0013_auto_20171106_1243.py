# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 12:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0012_auto_20171105_0841'),
    ]

    operations = [
        migrations.RenameField(
            model_name='session',
            old_name='startTime',
            new_name='start_time',
        ),
    ]