# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import image_cropping.fields
import apps.core.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('email', models.EmailField(null=True, max_length=255, blank=True, unique=True, verbose_name=b'Email', db_index=True)),
                ('username', models.CharField(unique=True, max_length=50, verbose_name=b'Nome')),
                ('slug', models.SlugField(max_length=150, blank=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'Ativo?')),
                ('is_member', models.BooleanField(default=True, verbose_name=b'Membro?')),
                ('is_superuser', models.BooleanField(default=False, verbose_name=b'Administrador?')),
                ('created_date', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Criado em')),
                ('photo', models.ImageField(upload_to=apps.core.models.update_filename, null=True, verbose_name=b'Foto', blank=True)),
                (b'photo_thumb', image_cropping.fields.ImageRatioField(b'photo', '65x65', hide_image_field=False, size_warning=False, allow_fullsize=False, free_crop=False, adapt_rotation=False, help_text=None, verbose_name='photo thumb')),
            ],
            options={
                'verbose_name': 'Usu\xe1rio',
                'verbose_name_plural': 'Usu\xe1rios',
            },
        ),
    ]
