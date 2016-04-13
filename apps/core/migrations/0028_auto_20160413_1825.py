# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_auto_20160411_2050'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='status_link',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='status_link',
            field=models.BooleanField(default=True),
        ),
    ]
