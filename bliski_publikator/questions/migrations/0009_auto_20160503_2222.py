# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-03 22:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0008_auto_20160503_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='description',
            field=models.TextField(blank=True, verbose_name='Description'),
        ),
    ]