# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20160329_2121'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='content_type',
        ),
        migrations.RemoveField(
            model_name='history',
            name='object_id',
        ),
        migrations.AddField(
            model_name='history',
            name='icon',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
