# -*- coding: utf-8 -*-
from django import forms

from apps.core.models import Folder, File


class LoginForm(forms.Form):
    name = forms.CharField(label=('Usuário'))
    password = forms.CharField(label=('Senha'), widget=forms.PasswordInput)
    remember_me = forms.CheckboxInput()


class FolderForm(forms.ModelForm):
    class Meta:
        model = Folder
        fields = ['name', 'permission']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']
