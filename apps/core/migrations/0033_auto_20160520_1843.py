# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0032_informative'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='folder',
            name='users',
        ),
        migrations.AddField(
            model_name='folder',
            name='users_read',
            field=models.ManyToManyField(related_name='shares_readonly', null=True, verbose_name=b'Com permiss\xc3\xa3o de leitura', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='users_write',
            field=models.ManyToManyField(related_name='shares_write', null=True, verbose_name=b'Com permiss\xc3\xa3o de escrita', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
