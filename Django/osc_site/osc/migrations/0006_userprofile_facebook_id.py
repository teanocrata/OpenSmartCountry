# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-05 18:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('osc', '0005_auto_20161204_0141'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='facebook_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
