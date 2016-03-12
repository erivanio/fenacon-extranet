# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_auto_20160312_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='areas',
            field=models.ManyToManyField(to='core.Area', verbose_name=b'areas'),
        ),
    ]
