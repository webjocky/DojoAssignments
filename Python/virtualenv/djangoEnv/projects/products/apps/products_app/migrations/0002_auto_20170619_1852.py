# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.CharField(default='food', max_length=40),
        ),
        migrations.AddField(
            model_name='product',
            name='cost',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='description',
            field=models.TextField(default='white socks'),
        ),
        migrations.AddField(
            model_name='product',
            name='name',
            field=models.CharField(default='socks', max_length=40),
        ),
        migrations.AddField(
            model_name='product',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.IntegerField(default=0),
        ),
    ]