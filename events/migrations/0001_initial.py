# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-05 20:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('date_start', models.DateField(verbose_name='Starts on')),
                ('time_start', models.TimeField(blank=True, null=True, verbose_name='Starts at')),
                ('date_end', models.DateField(blank=True, verbose_name='Ends on')),
                ('time_end', models.TimeField(blank=True, null=True, verbose_name='Ends at')),
                ('is_multi_day', models.BooleanField(default=False)),
                ('location', models.CharField(blank=True, max_length=50)),
                ('details', models.TextField(blank=True)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='events', to='categories.Category')),
            ],
            options={
                'ordering': ('-date_start', '-time_start'),
            },
        ),
    ]
