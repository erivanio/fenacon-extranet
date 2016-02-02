# -*- coding: utf-8 -*-
from django import forms
from apps.core.models import Folder, File, User


class LoginForm(forms.Form):
    name = forms.CharField(label=('Usuário'))
    password = forms.CharField(label=('Senha'), widget=forms.PasswordInput)
    remember_me = forms.CheckboxInput()


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser')

    def clean(self):
        password1 = self.data.get("password1")
        password2 = self.data.get("password2")

        if password1 and password1 != password2:
            raise forms.ValidationError("Senhas não conferem!")

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

    # def __init__(self, *args, **kwargs):
    #     self.bill_id = kwargs.pop('bill_id')
    #     super(FileForm, self).__init__(*args, **kwargs)
    #     self.fields['folder'].queryset = Folder.objects.filter(user=True)

    class Meta:
        model = File
        fields = ['name', 'file', 'folder']

