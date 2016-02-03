# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20160203_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='folder',
            old_name='folder',
            new_name='parent',
        ),
    ]
