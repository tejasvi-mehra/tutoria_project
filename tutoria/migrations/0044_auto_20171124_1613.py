# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-24 16:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0043_auto_20171124_1611'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='end_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='start_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='notification',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutoria.Student'),
        ),
        migrations.AddField(
            model_name='notification',
            name='tutor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tutoria.Tutor'),
        ),
        migrations.AddField(
            model_name='notification',
            name='viewed_stu',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='notification',
            name='viewed_tut',
            field=models.BooleanField(default=False),
        ),
    ]
