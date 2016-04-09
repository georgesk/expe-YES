# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-04-09 22:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    replaces = [('srv', '0001_initial'), ('srv', '0002_auto_20160409_2204')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Resa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('beg', models.TimeField()),
                ('end', models.TimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]