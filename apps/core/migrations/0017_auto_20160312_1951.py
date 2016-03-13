# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_user_areas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='areas',
            field=models.ManyToManyField(to='core.Area', null=True, verbose_name=b'areas', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', null=True, verbose_name=b'Permiss\xc3\xb5es', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='areas',
            field=models.ManyToManyField(related_name='permission_areas', null=True, verbose_name=b'areas', to='core.Area', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='core.Group', null=True, verbose_name=b'Grupos', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', null=True, verbose_name=b'Permiss\xc3\xb5es', blank=True),
        ),
    ]
