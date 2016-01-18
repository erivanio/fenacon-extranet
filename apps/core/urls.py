# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps.core.views import LogoutView, LoginView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^index/$', TemplateView.as_view(template_name='index2.html'), name='dashboard'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
)
