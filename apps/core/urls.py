# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from apps.core.views import LogoutView, LoginView, DashboardDetailView, FileCreateView, \
    FolderDetailView, AreaDetailView, AreaCreateView, UserCreateView, UserEditView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^(?P<slug>[\w_-]+)/$', DashboardDetailView.as_view(), name='dashboard'),
    url(r'^(?P<slug>[\w_-]+)/editar/', UserEditView.as_view(), name='edit_user'),
    url(r'^arquivo/adicionar-arquivo/', FileCreateView.as_view(), name='add_file'),
    url(r'^adicionar-usuario/', UserCreateView.as_view(), name='create_user'),
    url(r'^pasta/criar-pasta/$', 'apps.core.views.create_folder', name='create_folder'),
    url(r'^pasta/pasta-listar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/', FolderDetailView.as_view(), name='detail_folder'),
    url(r'^area/area-listar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/', AreaDetailView.as_view(), name='detail_area'),
    url(r'^area/criar-area/$', AreaCreateView.as_view(), name='create_area'),
)
