# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-17 14:25
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0007_auto_20190817_1420'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
        migrations.AddField(
            model_name='user',
            name='displayName',
            field=models.CharField(default='mohammad', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='outBooks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='reservedBooks',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='identityNumber',
            field=models.CharField(max_length=10, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=11, unique=True),
        ),
    ]
