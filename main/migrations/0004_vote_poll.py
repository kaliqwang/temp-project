# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 23:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20160713_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='vote',
            name='poll',
            field=models.ForeignKey(blank=True, default=0, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='votes', to='main.Poll'),
        ),
    ]