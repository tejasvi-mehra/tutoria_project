# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-21 13:03
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0029_auto_20171121_1258'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tutor',
            name='phoneNumber',
        ),
    ]