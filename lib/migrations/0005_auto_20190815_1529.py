# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-15 15:29
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0004_auto_20190815_1400'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='backDate',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]