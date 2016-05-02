from annoying.decorators import ajax_request
from apps.core.models import Folder, File, History
from datetime import datetime

@ajax_request
def status_link_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    if folder.status_link:
        folder.status_link = False
    else:
        folder.status_link = True
    folder.save()
    return folder.status_link


@ajax_request
def status_link_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    if file.status_link:
        file.status_link = False
    else:
        file.status_link = True
    file.save()
    return file.status_link


@ajax_request
def remove_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = False
    folder.deleted_at = datetime.now()
    folder.save()
    history = History()
    history.created_at = datetime.now()
    history.icon = 'fa-folder'
    history.content = '<a href="%s">%s</a> removeu a pasta "%s"' % (request.user.get_absolute_url(), request.user.get_display_name(), folder.name)
    history.save()


@ajax_request
def remove_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = False
    file.deleted_at = datetime.now()
    file.save()
    history = History()
    history.created_at = datetime.now()
    history.icon = 'fa-file'
    history.content = '<a href="%s">%s</a> removeu o arquivo "%s"' % (request.user.get_absolute_url(), request.user.get_display_name(), file.name)
    history.save()


@ajax_request
def add_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = True
    folder.deleted_at = None
    folder.save()
    history = History()
    history.created_at = datetime.now()
    history.icon = 'fa-folder'
    history.content = '<a href="%s">%s</a> restaurou a pasta "%s"' % (request.user.get_absolute_url(), request.user.get_display_name(), folder.name)
    history.save()


@ajax_request
def add_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = True
    file.deleted_at = None
    file.save()
    history = History()
    history.created_at = datetime.now()
    history.icon = 'fa-file'
    history.content = '<a href="%s">%s</a> restaurou o arquivo "%s"' % (request.user.get_absolute_url(), request.user.get_display_name(), file.name)
    history.save()
