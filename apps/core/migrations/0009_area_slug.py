# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20160203_1319'),
    ]

    operations = [
        migrations.AddField(
            model_name='area',
            name='slug',
            field=models.SlugField(max_length=150, blank=True),
        ),
    ]
