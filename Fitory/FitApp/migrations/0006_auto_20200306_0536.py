# -*- coding: utf-8 -*-
# Generated by Django 1.11.28 on 2020-03-06 05:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FitApp', '0005_auto_20190813_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='club',
            name='foto',
            field=models.ImageField(default='default/club.png', upload_to='usuarios/'),
        ),
    ]