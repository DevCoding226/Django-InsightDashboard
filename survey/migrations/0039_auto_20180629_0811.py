# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-06-29 08:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0038_question_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='unit',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='Unit'),
        ),
    ]