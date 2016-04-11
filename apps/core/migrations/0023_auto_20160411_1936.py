# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_user_receive_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='cpf',
            field=models.CharField(default=99999999999, max_length=11, verbose_name=b'CPF'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=11, null=True, verbose_name=b'Celular', blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(default=None, max_length=255, verbose_name=b'Email'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(default=None, max_length=50, verbose_name=b'Primeiro nome'),
            preserve_default=False,
        ),
    ]
