# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from apps.financier.views import TravelRefundCreateView, TravelRefundListView, \
    TravelRefundUpdateView, TravelRefundDeleteView, TravelRefundPDFView

urlpatterns = patterns('',
                       url(r'^solicitacao-reembolso/$',
                           TravelRefundCreateView.as_view(), name='create_refund'),
                       url(r'^solicitacao-reembolso-pdf/(?P<pk>\d+)/$',
                           TravelRefundPDFView.as_view(), name='refund_pdf'),
                       url(r'^solicitacao-reembolso/editar/(?P<pk>\d+)/$',
                           TravelRefundUpdateView.as_view(), name='update_refund'),
                       url(r'^listar-reembolsos/$',
                           TravelRefundListView.as_view(), name='list_refund'),
                       url(r'^solicitacao-reembolso/deletar/(?P<pk>\d+)/$',
                           TravelRefundDeleteView.as_view(), name='delete_refund'),
                       )
