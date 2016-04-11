# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20160411_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='cpf',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(unique=True, max_length=11, verbose_name=b'CPF'),
        ),
    ]
