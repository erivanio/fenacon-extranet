# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20160203_1033'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('name', models.CharField(max_length=200, verbose_name=b'Nome')),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': '\xc1rea',
                'verbose_name_plural': '\xc1reas',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Primeiro nome', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='job',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Cargo', blank=True),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name=b'Sobrenome', blank=True),
        ),
        migrations.AddField(
            model_name='area',
            name='user',
            field=models.ForeignKey(verbose_name=b'Usu\xc3\xa1rio', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='file',
            name='area',
            field=models.ForeignKey(verbose_name=b'\xc3\x81rea', blank=True, to='core.Area', null=True),
        ),
        migrations.AddField(
            model_name='folder',
            name='area',
            field=models.ForeignKey(verbose_name=b'\xc3\x81rea', blank=True, to='core.Area', null=True),
        ),
    ]
