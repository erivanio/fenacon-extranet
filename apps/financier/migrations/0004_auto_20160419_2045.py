# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('financier', '0003_auto_20160415_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='travelrefund',
            name='approved_by',
            field=models.ForeignKey(related_name='aproves', verbose_name=b'Aprovado por', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='travelrefund',
            name='beneficiary',
            field=models.ForeignKey(related_name='refund_beneficiary', verbose_name=b'Benefici\xc3\xa1rio', to=settings.AUTH_USER_MODEL),
        ),
    ]
