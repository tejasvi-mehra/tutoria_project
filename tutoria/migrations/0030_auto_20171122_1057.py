# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-22 10:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0029_coupon'),
    ]

    operations = [
        migrations.CreateModel(
            name='MyTutorsWallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='mytutors', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.DeleteModel(
            name='AdminWallet',
        ),
        migrations.AlterField(
            model_name='coupon',
            name='discount',
            field=models.IntegerField(),
        ),
    ]