# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0021_auto_20160405_2242'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='receive_email',
            field=models.BooleanField(default=False, verbose_name=b'Receber notifica\xc3\xa7\xc3\xa3o de reembolso?'),
        ),
    ]
