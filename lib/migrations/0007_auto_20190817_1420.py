# -*- coding: utf-8 -*-
# Generated by Django 1.11.21 on 2019-08-17 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0006_auto_20190815_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('password', models.CharField(max_length=16)),
                ('phone', models.CharField(max_length=10)),
                ('identityNumber', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('balance', models.IntegerField(default=0)),
            ],
        ),
        migrations.AlterField(
            model_name='book',
            name='backDate',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
