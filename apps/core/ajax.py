from annoying.decorators import ajax_request
from apps.core.models import Folder, File


@ajax_request
def remove_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = False
    folder.save()


@ajax_request
def remove_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = False
    file.save()


@ajax_request
def add_status_folder(request, folder_pk=None):
    folder = Folder.objects.get(pk=folder_pk)
    folder.status = True
    folder.save()


@ajax_request
def add_status_file(request, file_pk=None):
    file = File.objects.get(pk=file_pk)
    file.status = True
    file.save()
