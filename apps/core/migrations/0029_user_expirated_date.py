# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20160413_1825'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expirated_date',
            field=models.DateField(null=True, verbose_name=b'Expirar em', blank=True),
        ),
    ]
