# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20160216_1513'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome')),
                ('slug', models.SlugField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome')),
                ('slug', models.SlugField(max_length=150, blank=True)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name': 'Grupo',
                'verbose_name_plural': 'Grupos',
            },
        ),
        migrations.AddField(
            model_name='group',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', verbose_name=b'Permiss\xc3\xb5es'),
        ),
        migrations.AddField(
            model_name='user',
            name='permissions',
            field=models.ManyToManyField(to='core.Permission', verbose_name=b'Permiss\xc3\xb5es'),
        ),
    ]
