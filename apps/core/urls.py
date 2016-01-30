# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.core.views import LogoutView, LoginView, DashboardDetailView, FolderCreateView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(?P<slug>[\w_-]+)/$', DashboardDetailView.as_view(), name='dashboard'),
    url(r'^pasta/criar$', FolderCreateView.as_view(), name='create_folder'),
)
