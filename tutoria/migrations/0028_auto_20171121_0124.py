# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 01:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0027_wallet'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='tutor',
            name='balance',
        ),
    ]
