# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2019-07-19 15:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('FitApp', '0002_auto_20190719_1536'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscripcionfree',
            name='cliente',
        ),
        migrations.RemoveField(
            model_name='subscripcionfree',
            name='sucursal',
        ),
        migrations.DeleteModel(
            name='SubscripcionFree',
        ),
    ]