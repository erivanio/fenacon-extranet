# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20160204_2001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='area',
            name='name',
            field=models.CharField(unique=True, max_length=200, verbose_name=b'Nome'),
        ),
        migrations.AlterField(
            model_name='area',
            name='slug',
            field=models.SlugField(unique=True, max_length=150, blank=True),
        ),
    ]
