# -*- coding: utf-8 -*-
from django import forms
from apps.core.models import Folder, File, User, Area


class LoginForm(forms.Form):
    name = forms.CharField(label=('Usuário'))
    password = forms.CharField(label=('Senha'), widget=forms.PasswordInput)
    remember_me = forms.CheckboxInput()


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_superuser', 'first_name', 'last_name', 'job')

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
        fields = ['email', 'photo', 'first_name', 'last_name', 'job']


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


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ['name']

