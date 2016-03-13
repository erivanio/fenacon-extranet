# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_user_groups'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='areas',
            field=models.ManyToManyField(related_name='permission_areas', verbose_name=b'areas', to='core.Area'),
        ),
    ]
