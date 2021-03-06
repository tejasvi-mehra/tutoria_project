# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-25 10:52
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0006_auto_20171016_1527'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('startTime', models.DateTimeField(blank=True, null=True)),
                ('endTime', models.DateTimeField(blank=True, null=True)),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoria.Student')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tutoria.Tutor')),
            ],
        ),
        migrations.RenameModel(
            old_name='Transactions',
            new_name='Transaction',
        ),
    ]
