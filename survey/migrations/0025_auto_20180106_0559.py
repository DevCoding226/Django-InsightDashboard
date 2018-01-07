# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-06 05:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0024_auto_20180105_0433'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='survey.Question'),
        ),
    ]