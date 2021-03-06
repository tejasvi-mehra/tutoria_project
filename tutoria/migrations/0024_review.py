# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-11 19:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0023_auto_20171111_1651'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=250)),
                ('rating', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoria.Student')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoria.Tutor')),
            ],
        ),
    ]
