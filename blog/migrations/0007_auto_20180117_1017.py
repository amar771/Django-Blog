# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-01-17 10:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_me_isactive'),
    ]

    operations = [
        migrations.RenameField(
            model_name='me',
            old_name='isActive',
            new_name='is_active',
        ),
    ]