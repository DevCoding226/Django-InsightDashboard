# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-29 10:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20171226_2047'),
        ('survey', '0019_auto_20171228_0454'),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='countries',
            field=models.ManyToManyField(related_name='surveys', to='users.Country'),
        ),
    ]
