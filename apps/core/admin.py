# -*- coding: utf-8 -*-
from django.contrib import admin
from apps.core.models import Permission, User, Group

admin.site.register(Permission)
admin.site.register(User)
admin.site.register(Group)
