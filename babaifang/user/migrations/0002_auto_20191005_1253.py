# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2019-10-05 04:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='phone',
            field=models.IntegerField(),
        ),
    ]
