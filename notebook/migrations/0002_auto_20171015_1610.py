# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-10-15 16:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notebook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='intensive_passwd',
            field=models.CharField(max_length=30, null=True),
        ),
    ]