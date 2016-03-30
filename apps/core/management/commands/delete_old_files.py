# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from apps.core.models import File, Folder


class Command(BaseCommand):
    def handle(self, *args, **options):
        files_to_delete = File.objects.filter(deleted_at__isnull=False, deleted_at__gte=datetime.now()-timedelta(days=30))
        folders_to_delete = Folder.objects.filter(deleted_at__isnull=False, deleted_at__gte=datetime.now()-timedelta(days=30))
        for file in files_to_delete:
            file.delete()
        for folder in folders_to_delete:
            for obj in folder.folder_set.all():
                obj.delete()
            for obj in folder.file_set.all():
                obj.delete()