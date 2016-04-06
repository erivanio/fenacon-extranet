# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_auto_20160401_1521'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission',
            options={'ordering': ['name'], 'verbose_name': 'Permiss\xe3o', 'verbose_name_plural': 'Permiss\xf5es'},
        ),
    ]
