# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_auto_20160312_1951'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='deleted_at',
            field=models.DateTimeField(null=True, verbose_name=b'Data de dele\xc3\xa7\xc3\xa3o', blank=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='deleted_at',
            field=models.DateTimeField(null=True, verbose_name=b'Data de dele\xc3\xa7\xc3\xa3o', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='areas',
            field=models.ManyToManyField(to='core.Area', verbose_name=b'areas', blank=True),
        ),
        migrations.AlterField(
            model_name='group',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', verbose_name=b'Permiss\xc3\xb5es', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='areas',
            field=models.ManyToManyField(related_name='permission_areas', verbose_name=b'areas', to='core.Area', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(to='core.Group', verbose_name=b'Grupos', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', verbose_name=b'Permiss\xc3\xb5es', blank=True),
        ),
    ]
