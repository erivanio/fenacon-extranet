from annoying.decorators import ajax_request
from apps.core.models import Folder, File
from datetime import datetime

@ajax_request
def remove_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = False
    folder.deleted_at = datetime.now
    folder.save()


@ajax_request
def remove_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = False
    file.deleted_at = datetime.now
    file.save()


@ajax_request
def add_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = True
    folder.deleted_at = None
    folder.save()


@ajax_request
def add_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = True
    file.deleted_at = None
    file.save()
