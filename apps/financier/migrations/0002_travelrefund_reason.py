# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('financier', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelrefund',
            name='reason',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
