# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-21 00:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0026_auto_20171120_1343'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
    ]
