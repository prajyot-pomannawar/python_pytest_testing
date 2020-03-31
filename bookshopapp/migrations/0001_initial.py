# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-03-26 09:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('author', models.CharField(max_length=50)),
                ('publication', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=50)),
                ('isbn', models.IntegerField()),
                ('price', models.IntegerField()),
            ],
            options={
                'db_table': 'books',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=50)),
                ('lname', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'users',
            },
        ),
    ]