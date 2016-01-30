# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20160120_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, null=True, verbose_name=b'Nome', blank=True)),
                ('file', models.FileField(upload_to=b'uploads/files/')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Publica\xc3\xa7\xc3\xa3o')),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Arquivo',
                'verbose_name_plural': 'Arquivos',
            },
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Publica\xc3\xa7\xc3\xa3o')),
                ('status', models.BooleanField(default=True)),
                ('permission', models.CharField(default=b'public', max_length=10, choices=[(b'public', b'P\xc3\xbablico'), (b'private', b'Somente eu')])),
                ('user', models.ForeignKey(verbose_name=b'Usu\xc3\xa1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Pastas',
                'verbose_name_plural': 'Pastas',
            },
        ),
        migrations.AddField(
            model_name='file',
            name='folder',
            field=models.ForeignKey(verbose_name=b'Pasta', to='core.Folder'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(verbose_name=b'Usu\xc3\xa1rio', to=settings.AUTH_USER_MODEL),
        ),
    ]
