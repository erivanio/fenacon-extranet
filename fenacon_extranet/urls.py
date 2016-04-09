from django.conf.urls import include, url, patterns
from django.contrib import admin
from apps.core.views import PasswordResetUnregister
from fenacon_extranet import settings

urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^financeiro/', include('apps.financier.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
    url(r'^password_change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password_change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password_reset/$', 'apps.core.views.password_reset', name='password_reset'),
    url(r'^password_reset/unregister/$', PasswordResetUnregister.as_view(), name='password_reset_unregister'),
    url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        name='password_reset_confirm'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
]

urlpatterns += patterns('',
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^ckeditor/', include('ckeditor.urls')),
)