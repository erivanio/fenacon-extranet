# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.financier.views import TravelRefundCreateView, TravelRefundListView, TravelRefundUpdateView

urlpatterns = patterns('',
    url(r'^solicitacao-reembolso/$', TravelRefundCreateView.as_view(), name='create_refund'),
    url(r'^solicitacao-reembolso/editar/(?P<pk>\d+)/$', TravelRefundUpdateView.as_view(), name='update_refund'),
    url(r'^listar-reembolsos/$', TravelRefundListView.as_view(), name='list_refund'),
)
