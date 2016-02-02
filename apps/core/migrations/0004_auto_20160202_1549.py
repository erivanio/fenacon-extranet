# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('core', '0003_auto_20160130_1337'),
    ]

    operations = [
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('object_id', models.PositiveIntegerField()),
                ('content', models.TextField(verbose_name=b'Conte\xc3\xbado')),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('user', models.ForeignKey(verbose_name=b'Usu\xc3\xa1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['created_at'],
                'verbose_name': 'Hist\xf3rico',
                'verbose_name_plural': 'Hist\xf3ricos',
            },
        ),
        migrations.AddField(
            model_name='folder',
            name='slug',
            field=models.SlugField(max_length=150, blank=True),
        ),
    ]
