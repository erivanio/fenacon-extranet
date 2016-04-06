# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TravelRefund',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('authorizer', models.CharField(max_length=200, verbose_name=b'Autorizador')),
                ('going_date', models.DateField(verbose_name=b'Data')),
                ('going_enterprise', models.CharField(max_length=200, verbose_name=b'Empresa')),
                ('going_exit_time', models.TimeField(verbose_name=b'Data de sa\xc3\xadda', blank=True)),
                ('going_arrival_time', models.TimeField(verbose_name=b'Data de chegada', blank=True)),
                ('back_date', models.DateField(verbose_name=b'Data')),
                ('back_enterprise', models.CharField(max_length=200, verbose_name=b'Empresa')),
                ('back_exit_time', models.TimeField(verbose_name=b'Data de sa\xc3\xadda', blank=True)),
                ('back_arrival_time', models.TimeField(verbose_name=b'Data de chegada', blank=True)),
                ('expenses_locomotion', models.FloatField(null=True, verbose_name=b'Despesas com locomo\xc3\xa7\xc3\xa3o', blank=True)),
                ('meal_expenses', models.FloatField(null=True, verbose_name=b'Despesas com refei\xc3\xa7\xc3\xa3o', blank=True)),
                ('daily', models.FloatField(null=True, verbose_name=b'Di\xc3\xa1ria', blank=True)),
                ('mileage', models.FloatField(null=True, verbose_name=b'Quilometragem', blank=True)),
                ('history', models.TextField(null=True, verbose_name=b'Hist\xc3\xb3rico', blank=True)),
                ('status', models.CharField(default=b'1', max_length=10, choices=[(b'1', b'Aguardando'), (b'2', b'Aprovada'), (b'3', b'Pago'), (b'4', b'Rejeitada')])),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Data de Cria\xc3\xa7\xc3\xa3o')),
                ('beneficiary', models.ForeignKey(verbose_name=b'Benefici\xc3\xa1rio', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
                'verbose_name': 'Reembolso de Viagem',
                'verbose_name_plural': 'Reembolsos de Viagens',
            },
        ),
    ]
