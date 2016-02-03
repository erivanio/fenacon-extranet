# -*- coding: utf-8 -*-
from datetime import datetime
import os
import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models
from django.db.models import signals
from django.utils.text import slugify
from easy_thumbnails.files import get_thumbnailer
from image_cropping import ImageRatioField


class UserManager(BaseUserManager):
    def create_user(self, username, password=None):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password=password)
        user.is_superuser = True
        user.save(using=self._db)
        return user


def update_filename(instance, filename):
    path = "uploads/user/"
    fname = filename.split('.')
    format = slugify(fname[0]) + ''.join([random.SystemRandom().choice(''.join(string.digits)) for i in range(8)]) + '.' + fname[-1]
    return os.path.join(path, format)


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    email = models.EmailField(verbose_name='Email', max_length=255, unique=True, db_index=True, blank=True, null=True)
    username = models.CharField('Nome', max_length=50, unique=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    is_active = models.BooleanField('Ativo?', default=True)
    is_member = models.BooleanField('Membro?', default=True)
    is_superuser = models.BooleanField('Administrador?', default=False)
    created_date = models.DateTimeField('Criado em', default=datetime.now)
    photo = models.ImageField('Foto', upload_to=update_filename, blank=True, null=True)
    photo_thumb = ImageRatioField('photo', '65x65')
    objects = UserManager()

    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS = ['username']

    def get_photo_thumb(self):
        return get_thumbnailer(self.photo).get_thumbnail({
            'size': (65, 65),
            'box': self.photo_thumb,
            'crop': True,
            'detail': True,
            }).url

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __unicode__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_superuser


def user_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.username)

signals.pre_save.connect(user_pre_save, sender=User)


class Folder(models.Model):
    PERMISSION_FOLDER = (
        ('public', 'Público'),
        ('private', 'Somente eu')
    )
    folder = models.ForeignKey('self', related_name='children', verbose_name='Pasta', null=True, blank=True)
    name = models.CharField('Nome', max_length=200)
    created_at = models.DateTimeField(verbose_name='Data de Publicação', default=datetime.now)
    user = models.ForeignKey(User, verbose_name='Usuário')
    status = models.BooleanField(default=True)
    permission = models.CharField(max_length=10, choices=PERMISSION_FOLDER, default='public')
    slug = models.SlugField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Pastas'
        verbose_name_plural = 'Pastas'
        ordering = ['name']

    def __unicode__(self):
        return self.name


def folder_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

signals.pre_save.connect(folder_pre_save, sender=Folder)


class File(models.Model):
    name = models.CharField('Nome', max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='uploads/files/')
    folder = models.ForeignKey(Folder, verbose_name='Pasta')
    created_at = models.DateTimeField(verbose_name='Data de Publicação', default=datetime.now)
    user = models.ForeignKey(User, verbose_name='Usuário')
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'
        ordering = ['created_at']

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return u'%s' % str(self.file).split('/')[-1]


class History(models.Model):
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)
    user = models.ForeignKey(User, verbose_name='Usuário')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey('contenttypes.ContentType')
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField('Conteúdo')

    class Meta:
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'
        ordering = ['created_at']

    def __unicode__(self):
        return self.user
