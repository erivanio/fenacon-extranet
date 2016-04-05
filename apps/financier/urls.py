# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.financier.views import TravelRefundCreateView

urlpatterns = patterns('',
    url(r'^criar-reembolso/$', TravelRefundCreateView.as_view(), name='create_refund'),
)
