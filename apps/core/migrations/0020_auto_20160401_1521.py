# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_auto_20160401_1508'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='history',
            options={'ordering': ['-created_at'], 'verbose_name': 'Hist\xf3rico', 'verbose_name_plural': 'Hist\xf3ricos'},
        ),
        migrations.RemoveField(
            model_name='history',
            name='user',
        ),
    ]
