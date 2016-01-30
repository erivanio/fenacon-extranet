from django.conf.urls import include, url, patterns
from django.contrib import admin
from fenacon_extranet import settings

urlpatterns = [
    url(r'^', include('apps.core.urls')),
    url(r'^admin/', include(admin.site.urls), name='admin'),
]

urlpatterns += patterns('',
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^ckeditor/', include('ckeditor.urls')),
)