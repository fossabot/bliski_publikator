# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-04 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('monitorings', '0005_auto_20160503_2222'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitoring',
            name='max_point',
            field=models.IntegerField(default=250, verbose_name='Max point'),
            preserve_default=False,
        ),
    ]
