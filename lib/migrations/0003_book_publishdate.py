# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-13 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0002_auto_20190813_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='publishdate',
            field=models.CharField(default='\u0628\u0647\u0627\u0631 1390', max_length=50),
        ),
    ]