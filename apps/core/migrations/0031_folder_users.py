# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0030_history_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='users',
            field=models.ManyToManyField(related_name='shares', null=True, verbose_name=b'Compartilhar com', to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
