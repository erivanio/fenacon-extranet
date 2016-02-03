# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.core.views import LogoutView, LoginView, DashboardDetailView, FolderCreateView, FolderListView, FileCreateView, \
    FolderDetailView, AreaDetailView, AreaCreateView, UserCreateView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(?P<slug>[\w_-]+)/$', DashboardDetailView.as_view(), name='dashboard'),
    url(r'^arquivo/adicionar', FileCreateView.as_view(), name='add_file'),
    url(r'^usuario/adicionar', UserCreateView.as_view(), name='create_user'),
    url(r'^pasta/criar$', FolderCreateView.as_view(), name='create_folder'),
    url(r'^pasta/(?P<folder_slug>[\w_-]+)-(?P<folder_id>\d+)/arquivos', FolderDetailView.as_view(), name='detail_folder'),
    url(r'^pasta/listagem', FolderListView.as_view(), name='list_folder'),
    url(r'^area/(?P<area_slug>[\w_-]+)-(?P<area_id>\d+)', AreaDetailView.as_view(), name='detail_area'),
   url(r'^area/criar$', AreaCreateView.as_view(), name='create_area'),
)
