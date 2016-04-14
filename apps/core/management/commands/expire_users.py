# -*- coding: utf-8 -*-
from datetime import datetime, timedelta, date
from django.core.management.base import BaseCommand
from apps.core.models import File, Folder, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        users_to_expire = User.objects.filter(is_active=True, expirated_date__lte=date.today())
        for user in users_to_expire:
            user.is_active = False
            user.save()