# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-08 10:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='avatar',
            field=models.FileField(upload_to='upload/avatar/', verbose_name='头像'),
        ),
    ]
