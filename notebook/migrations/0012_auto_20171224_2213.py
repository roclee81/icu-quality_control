# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-24 14:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0011_auto_20171130_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='passwd',
            field=models.CharField(max_length=25, null=True),
        ),
    ]