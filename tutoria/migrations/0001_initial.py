# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-09 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('biography', models.CharField(max_length=10000)),
                ('university', models.CharField(max_length=100)),
                ('tutortype', models.CharField(max_length=10)),
            ],
        ),
    ]
