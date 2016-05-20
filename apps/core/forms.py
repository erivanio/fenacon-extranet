# -*- coding: utf-8 -*-
from django import forms
from localflavor.br.forms import BRCPFField
from apps.core.models import Folder, User, Area, Group, File, Informative
import selectable.forms as selectable
from apps.core.lookups import UserLookup



class LoginForm(forms.Form):
    name = forms.CharField(label='Usuário')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)
    remember_me = forms.CheckboxInput()


class GroupCreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ('name', 'permissions', 'areas')


class UserCreateForm(forms.ModelForm):
    username = BRCPFField(max_length=14, min_length=11)

    class Meta:
        model = User
        fields = ('username', 'email', 'expirated_date', 'is_superuser', 'receive_email', 'first_name', 'last_name', 'telephone', 'job', 'groups', 'permissions', 'areas')

    def clean(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")
        username = self.data.get("username")

        if password1 and password1 != password2:
            raise forms.ValidationError("Senhas não conferem!")

        if username in User.objects.all().values_list('username', flat=True):
            raise forms.ValidationError("Este usuário já existe")

        if not username:
            raise forms.ValidationError("O campo usuário é obrigatório")

        if not password1 or not password2:
            raise forms.ValidationError("Digite uma senha e confirme")

        return self.cleaned_data

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.set_password(self.data["password1"])
        user.is_active = True
        if commit:
            user.save()
        return user


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'photo', 'telephone', 'first_name', 'last_name', 'job', 'expirated_date', 'receive_email', 'is_active', 'is_superuser', 'groups', 'permissions', 'areas']


class FolderForm(forms.ModelForm):
    PERMISSION_FOLDER = (
        ('public', 'Público'),
        ('private', 'Somente eu')
    )
    permission = forms.ChoiceField(choices=PERMISSION_FOLDER)
    users = selectable.AutoCompleteSelectMultipleField(
        lookup_class=UserLookup,
        label='Compartilhar com',
        required=False,
    )
    class Meta:
        model = Folder
        fields = ['name', 'permission', 'users']


class FileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name']


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name']


class InformativeForm(forms.ModelForm):
    class Meta:
        model = Informative
        fields = ['title', 'content', 'status']

