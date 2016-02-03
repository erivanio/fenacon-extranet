# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20160202_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='folder',
            field=models.ForeignKey(related_name='children', verbose_name=b'Pasta', blank=True, to='core.Folder', null=True),
        ),
    ]
