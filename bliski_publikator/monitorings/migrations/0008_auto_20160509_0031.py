# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-09 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('institutions', '0005_remove_institution_monitorings'),
        ('monitorings', '0007_remove_monitoring_institutions'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonitoringInstitution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('institution', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='institutions.Institution', verbose_name='Institution')),
            ],
            options={
                'verbose_name': 'Monitoring of institution',
                'verbose_name_plural': 'Monitorings of institutions',
            },
        ),
        migrations.AddField(
            model_name='monitoring',
            name='institutions',
            field=models.ManyToManyField(blank=True, help_text='Specifies which institutions are covered by monitoring', to='institutions.Institution', through='monitorings.MonitoringInstitution', verbose_name='Institution'),
        ),
        migrations.AddField(
            model_name='monitoringinstitution',
            name='monitoring',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='monitorings.Monitoring', verbose_name='Monitoring'),
        ),
    ]
