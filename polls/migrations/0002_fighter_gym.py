# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-06-20 07:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='gym',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
