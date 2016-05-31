# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0031_folder_users'),
    ]

    operations = [
        migrations.CreateModel(
            name='Informative',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200, null=True, verbose_name=b'T\xc3\xadtulo', blank=True)),
                ('content', models.TextField(null=True, verbose_name=b'Conte\xc3\xbado', blank=True)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Informativo',
                'verbose_name_plural': 'Informativos',
            },
        ),
    ]
