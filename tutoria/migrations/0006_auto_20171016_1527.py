# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-16 15:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tutoria', '0005_student_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='student',
            old_name='tutor',
            new_name='isTutor',
        ),
        migrations.RenameField(
            model_name='tutor',
            old_name='student',
            new_name='isStudent',
        ),
    ]
