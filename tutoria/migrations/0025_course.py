# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-20 13:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0024_review'),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default='', max_length=10)),
                ('subject', models.CharField(default='', max_length=100)),
            ],
        ),
    ]
