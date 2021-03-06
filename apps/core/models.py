# -*- coding: utf-8 -*-
from datetime import datetime
import hashlib
import os
import random
import string
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.urlresolvers import reverse
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


class Permission(models.Model):
    name = models.CharField('Nome', max_length=200)
    slug = models.SlugField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Permissão'
        verbose_name_plural = 'Permissões'
        ordering = ['name']

    def __unicode__(self):
        return self.name


def permission_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

signals.pre_save.connect(permission_pre_save, sender=Permission)


class Group(models.Model):
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)
    name = models.CharField('Nome', max_length=200)
    slug = models.SlugField(max_length=150, blank=True)
    permissions = models.ManyToManyField(Permission, verbose_name="Permissões", blank=True)
    areas = models.ManyToManyField('core.Area', verbose_name="areas", blank=True)
    areas_read = models.ManyToManyField('core.Area', related_name="group_onlyread_areas", verbose_name="areas", blank=True)

    class Meta:
        verbose_name = 'Grupo'
        verbose_name_plural = 'Grupos'
        ordering = ['name']

    def __unicode__(self):
        return self.name


def group_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

signals.pre_save.connect(group_pre_save, sender=Group)


class User(AbstractBaseUser):
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'

    first_name = models.CharField('Primeiro nome', max_length=50)
    last_name = models.CharField('Sobrenome', max_length=50, blank=True, null=True)
    job = models.CharField('Cargo', max_length=50, blank=True, null=True)
    email = models.EmailField(verbose_name='Email', max_length=255)
    telephone = models.CharField('Celular', max_length=15, blank=True, null=True)
    username = models.CharField('CPF', max_length=14, unique=True)
    slug = models.SlugField(max_length=150, blank=True, unique=True)
    receive_email = models.BooleanField('Receber notificação de reembolso?', default=False)
    is_active = models.BooleanField('Ativo?', default=True)
    is_member = models.BooleanField('Membro?', default=True)
    is_superuser = models.BooleanField('Administrador?', default=False)
    created_date = models.DateTimeField('Criado em', default=datetime.now)
    expirated_date = models.DateField('Expirar em', blank=True, null=True)
    photo = models.ImageField('Foto', upload_to=update_filename, blank=True, null=True)
    photo_thumb = ImageRatioField('photo', '65x65')
    permissions = models.ManyToManyField(Permission, verbose_name="Permissões", blank=True)
    groups = models.ManyToManyField(Group, verbose_name="Grupos", blank=True)
    areas = models.ManyToManyField('core.Area', related_name="permission_areas", verbose_name="areas", blank=True)
    areas_read = models.ManyToManyField('core.Area', related_name="onlyread_areas", verbose_name="areas", blank=True)
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

    def __unicode__(self):
        return self.get_display_name()

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        return ' '.join([self.first_name, self.last_name]).strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.first_name

    def get_display_name(self):
        if self.first_name and self.last_name:
            return self.get_full_name()
        elif self.first_name and not self.last_name:
            return self.get_short_name()
        else:
            return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return reverse('dashboard', kwargs={'slug': self.slug})

    @property
    def is_staff(self):
        return self.is_superuser


def user_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.username)

signals.pre_save.connect(user_pre_save, sender=User)


class Area(models.Model):
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)
    user = models.ForeignKey(User, verbose_name='Usuário')
    name = models.CharField('Nome', max_length=200)
    status = models.BooleanField(default=True)
    slug = models.SlugField(max_length=150, blank=True)

    class Meta:
        verbose_name = 'Área'
        verbose_name_plural = 'Áreas'
        ordering = ['created_at']

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail_area', kwargs={'slug': self.slug, 'pk': self.pk})


def area_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

signals.pre_save.connect(area_pre_save, sender=Area)


class Folder(models.Model):
    PERMISSION_FOLDER = (
        ('public', 'Público'),
        ('private', 'Somente eu')
    )
    parent = models.ForeignKey('self', related_name='children', verbose_name='Pasta', null=True, blank=True)
    area = models.ForeignKey(Area, verbose_name='Área', null=True, blank=True)
    name = models.CharField('Nome', max_length=200)
    created_at = models.DateTimeField(verbose_name='Data de Publicação', default=datetime.now)
    deleted_at = models.DateTimeField(verbose_name='Data de deleção', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuário')
    status = models.BooleanField(default=True)
    permission = models.CharField(max_length=10, choices=PERMISSION_FOLDER, default='public')
    slug = models.SlugField(max_length=150, blank=True)
    status_link = models.BooleanField(default=True)
    users_read = models.ManyToManyField(User, related_name='shares_readonly', verbose_name='Com permissão de leitura', blank=True)
    users_write = models.ManyToManyField(User, related_name='shares_write', verbose_name='Com permissão de escrita', blank=True)

    class Meta:
        verbose_name = 'Pastas'
        verbose_name_plural = 'Pastas'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def get_hash_slug(self):
        hash_object = hashlib.md5(self.slug)
        return hash_object.hexdigest()

    def get_absolute_url(self):
        return reverse('detail_folder', kwargs={'slug': self.slug, 'pk': self.pk})


def folder_pre_save(signal, instance, sender, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)

signals.pre_save.connect(folder_pre_save, sender=Folder)


class File(models.Model):
    name = models.CharField('Nome', max_length=200, blank=True, null=True)
    file = models.FileField(upload_to='uploads/files/')
    folder = models.ForeignKey(Folder, verbose_name='Pasta', blank=True, null=True)
    area = models.ForeignKey(Area, verbose_name='Área', null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Data de Publicação', default=datetime.now)
    deleted_at = models.DateTimeField(verbose_name='Data de deleção', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Usuário')
    status = models.BooleanField(default=True)
    status_link = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Arquivo'
        verbose_name_plural = 'Arquivos'
        ordering = ['created_at']

    def __unicode__(self):
        if self.name:
            return self.name
        else:
            return u'%s' % str(self.file).split('/')[-1]

    def get_hash_slug(self):
        hash_object = hashlib.md5(slugify(self.name))
        return hash_object.hexdigest()


def file_pre_save(signal, instance, sender, **kwargs):
    if not instance.name:
        instance.name = str(instance.file).split('/')[-1]

signals.pre_save.connect(file_pre_save, sender=File)


class History(models.Model):
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)
    content = models.TextField('Conteúdo')
    icon = models.CharField(max_length=200, null=True, blank=True)
    user = models.ForeignKey(User, null=True, blank=True)

    class Meta:
        verbose_name = 'Histórico'
        verbose_name_plural = 'Históricos'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.content



class Informative(models.Model):
    title = models.CharField('Título', max_length=200, null=True, blank=True)
    content = models.TextField('Conteúdo', null=True, blank=True)
    status = models.BooleanField(default=True)
    user = models.ForeignKey(User, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name='Data de Criação', default=datetime.now)

    class Meta:
        verbose_name = 'Informativo'
        verbose_name_plural = 'Informativos'
        ordering = ['-created_at']

    def __unicode__(self):
        return self.title
