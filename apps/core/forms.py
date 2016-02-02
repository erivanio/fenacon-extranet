# -*- coding: utf-8 -*-
from django import forms
from apps.core.models import Folder, File, User


class LoginForm(forms.Form):
    name = forms.CharField(label=('Usuário'))
    password = forms.CharField(label=('Senha'), widget=forms.PasswordInput)
    remember_me = forms.CheckboxInput()


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'photo']
    username = forms.CharField(label='Nome')


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'permission']

    PERMISSION_FOLDER = (
        ('public', 'Público'),
        ('private', 'Somente eu')
    )
    permission = forms.ChoiceField(choices=PERMISSION_FOLDER)


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

