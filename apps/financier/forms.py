# -*- coding: utf-8 -*-
from django import forms
from apps.financier.models import TravelRefund


class TravelRefundForm(forms.ModelForm):
    class Meta:
        model = TravelRefund
        exclude = ['created_at']
