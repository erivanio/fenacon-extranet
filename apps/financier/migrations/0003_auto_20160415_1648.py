# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financier', '0002_travelrefund_reason'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='travelrefund',
            name='authorizer',
        ),
        migrations.AddField(
            model_name='travelrefund',
            name='observation',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
