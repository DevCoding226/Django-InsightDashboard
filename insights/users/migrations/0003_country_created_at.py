# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-28 19:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20161228_1931'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Datetime of creation'),
        ),
    ]