# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-07-01 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0039_auto_20180629_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Submitted'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True, verbose_name='Organization name'),
        ),
    ]