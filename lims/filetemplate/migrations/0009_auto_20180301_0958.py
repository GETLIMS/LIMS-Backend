# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-03-01 09:58
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('filetemplate', '0008_filetemplate_total_inputs_only'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='filetemplate',
            options={'ordering': ['-id']},
        ),
    ]
