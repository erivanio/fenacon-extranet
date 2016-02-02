# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.core.views import LogoutView, LoginView, DashboardDetailView, FolderCreateView, FolderListView, FileCreateView, \
    FolderDetailView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(?P<slug>[\w_-]+)/$', DashboardDetailView.as_view(), name='dashboard'),
    url(r'^arquivo/adicionar', FileCreateView.as_view(), name='add_file'),
    url(r'^pasta/criar$', FolderCreateView.as_view(), name='create_folder'),
    url(r'^pasta/(?P<pk>[\d-]+)/arquivos', FolderDetailView.as_view(), name='detail_folder'),
    url(r'^pasta/listagem', FolderListView.as_view(), name='list_folder'),
)
