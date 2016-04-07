# -*- coding: utf-8 -*-
from datetime import date, datetime

from django.db import models

from apps.core.models import User


class TravelRefund(models.Model):
    STATUS_CHOICE = (
        ('1', 'Aguardando'),
        ('2', 'Aprovada'),
        ('3', 'Pago'),
        ('4', 'Rejeitada')
    )
    beneficiary = models.ForeignKey(User, verbose_name='Beneficiário')
    authorizer = models.CharField('Autorizador', max_length=200)
    going_date = models.DateField(verbose_name='Data')
    going_enterprise = models.CharField(verbose_name='Empresa', max_length=200)
    going_exit_time = models.TimeField(verbose_name='Data de saída', blank=True)
    going_arrival_time = models.TimeField(verbose_name='Data de chegada', blank=True)
    back_date = models.DateField(verbose_name='Data')
    back_enterprise = models.CharField(verbose_name='Empresa', max_length=200)
    back_exit_time = models.TimeField(verbose_name='Data de saída', blank=True)
    back_arrival_time = models.TimeField(verbose_name='Data de chegada', blank=True)
    expenses_locomotion = models.FloatField(verbose_name='Despesas com locomoção', null=True, blank=True)
    meal_expenses = models.FloatField(verbose_name='Despesas com refeição', null=True, blank=True)
    daily = models.FloatField(verbose_name='Diária', null=True, blank=True)
    mileage = models.FloatField(verbose_name='Quilometragem', null=True, blank=True)
    history = models.TextField(verbose_name='Histórico', null=True, blank=True)
    reason = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='1')
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)

    class Meta:
        verbose_name = 'Reembolso de Viagem'
        verbose_name_plural = 'Reembolsos de Viagens'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.beneficiary.get_display_name()
