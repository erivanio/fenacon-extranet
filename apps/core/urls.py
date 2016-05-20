# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from apps.core.views import LogoutView, LoginView, DashboardDetailView, \
    FolderDetailView, AreaDetailView, AreaCreateView, UserCreateView, UserEditView, GarbageDetailView, FileDeleteView, \
    FolderDeleteView, AreaUpdateView, FolderUpdateView, GroupCreateView, AreaDeleteView, UserListView, HistoryListView, \
    UserDeleteView, GroupUpdateView, MyActionsListView, FileUpdateView, InformativeUpdateView, InformativeCreateView, \
    InformativeDeleteView

urlpatterns = patterns('',
    url(r'^$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^status-link/folder/(?P<folder_pk>\d+)/$', 'apps.core.ajax.status_link_folder', name='link_folder'),
    url(r'^status-link/file/(?P<file_pk>\d+)/$', 'apps.core.ajax.status_link_file', name='link_file'),
    url(r'^pasta/restaurar/(?P<folder_pk>\d+)/$', 'apps.core.ajax.add_status_folder', name='add_folder'),
    url(r'^pasta/deletar/(?P<folder_pk>\d+)/$', 'apps.core.ajax.remove_status_folder', name='remove_folder'),
    url(r'^pasta/excluir/(?P<pk>\d+)/$', FolderDeleteView.as_view(), name='folder_delete'),
    url(r'^pasta/editar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/$', FolderUpdateView.as_view(), name='update_folder'),
    url(r'^pasta/criar-pasta/$', 'apps.core.views.create_folder', name='create_folder'),
    url(r'^pasta/pasta-listar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/', FolderDetailView.as_view(), name='detail_folder'),
    url(r'^arquivo/editar/(?P<pk>\d+)/$', FileUpdateView.as_view(), name='update_file'),
    url(r'^(?P<slug>[\w_-]+)/lixeira/$', GarbageDetailView.as_view(), name='garbage'),
    url(r'^usuario/deletar/(?P<pk>\d+)', UserDeleteView.as_view(), name='delete_user'),
    url(r'^usuario/(?P<slug>[\w_-]+)/editar/', UserEditView.as_view(), name='edit_user'),
    url(r'^usuario/novo/', UserCreateView.as_view(), name='create_user'),
    url(r'^usuario/lista/', UserListView.as_view(), name='list_user'),
    url(r'^grupo/novo/', GroupCreateView.as_view(), name='create_group'),
    url(r'^grupo/editar/(?P<pk>\d+)/', GroupUpdateView.as_view(), name='update_group'),
    url(r'^arquivo/adicionar-arquivo/', 'apps.core.views.create_file', name='create_file'),
    url(r'^arquivo/restaurar/(?P<file_pk>\d+)/$', 'apps.core.ajax.add_status_file', name='add_file'),
    url(r'^arquivo/deletar/(?P<file_pk>\d+)/$', 'apps.core.ajax.remove_status_file', name='remove_file'),
    url(r'^arquivo/excluir/(?P<pk>\d+)/$', FileDeleteView.as_view(), name='file_delete'),
    url(r'^area/area-listar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/', AreaDetailView.as_view(), name='detail_area'),
    url(r'^area-editar/(?P<slug>[\w_-]+)-(?P<pk>\d+)/$', AreaUpdateView.as_view(), name='update_area'),
    url(r'^area/criar-area/$', AreaCreateView.as_view(), name='create_area'),
    url(r'^area/deletar/(?P<pk>\d+)/$', AreaDeleteView.as_view(), name='delete_area'),
    url(r'^usuario/(?P<slug>[\w_-]+)/$', DashboardDetailView.as_view(), name='dashboard'),
    url(r'^historico/$', HistoryListView.as_view(), name='history'),
    url(r'^minhas-acoes/$', MyActionsListView.as_view(), name='my_actions'),
    url(r'^informativo/editar/(?P<pk>\d+)/$', InformativeUpdateView.as_view(), name='update_informative'),
    url(r'^informativo/criar/$', InformativeCreateView.as_view(), name='create_informative'),
    url(r'^informativo/deletar/(?P<pk>\d+)/$', InformativeDeleteView.as_view(), name='delete_informative'),
)
