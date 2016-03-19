# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=100)),
                ('last_name', models.CharField(max_length=100)),
                ('name_format', models.CharField(choices=[('us', 'First Name First'), ('jp', 'Last Name First')], max_length=3)),
            ],
        ),
    ]