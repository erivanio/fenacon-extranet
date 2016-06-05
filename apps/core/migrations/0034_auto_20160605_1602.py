# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0033_auto_20160520_1843'),
    ]

    operations = [
        migrations.AddField(
            model_name='group',
            name='areas_read',
            field=models.ManyToManyField(related_name='group_onlyread_areas', verbose_name=b'areas', to='core.Area', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='areas_read',
            field=models.ManyToManyField(related_name='onlyread_areas', verbose_name=b'areas', to='core.Area', blank=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='users_read',
            field=models.ManyToManyField(related_name='shares_readonly', verbose_name=b'Com permiss\xc3\xa3o de leitura', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='folder',
            name='users_write',
            field=models.ManyToManyField(related_name='shares_write', verbose_name=b'Com permiss\xc3\xa3o de escrita', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
