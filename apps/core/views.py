# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, CreateView, ListView, UpdateView
from apps.core.forms import LoginForm, FolderForm, FileForm, UserEditForm, UserCreateForm
from apps.core.models import User, Folder, File


class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        context['form'] = LoginForm()

        return context

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(29030400)
            u = authenticate(username=form.cleaned_data['name'], password=form.cleaned_data['password'])
            if u is not None:
                if u.is_active:
                    login(request, u)
                    return redirect('dashboard', slug=u.slug)
            messages.error(self.request, 'Usuário ou senha inválidos')

        return redirect('login')


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/user_create.html'

    def form_valid(self, form):
        form.save()
        return redirect('dashboard', pk=self.request.user.slug)


class UserEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user/user_edit.html'

    def get_object(self, *args, **kwargs):
        object = super(UserEditView, self).get_object(*args, **kwargs)
        if object != self.request.user:
            raise Http404
        return object

    def get_success_url(self):
        messages.success(self.request, 'Perfil modificado com sucesso!')
        return redirect('dashboard', pk=self.object.slug)


class DashboardDetailView(DetailView):
    model = User
    template_name = 'dashboard.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(DashboardDetailView, self).dispatch(*args, **kwargs)


class FolderCreateView(CreateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folder/create-folder.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(FolderCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        folder = Folder()
        folder.name = form.cleaned_data['name']
        folder.permission = form.cleaned_data['permission']
        folder.status = True
        folder.user = self.request.user
        folder.save()
        messages.success(self.request, 'Pasta criada com sucesso!')
        return redirect('dashboard', pk=folder.user.slug)

    def form_invalid(self, form):
        if 'name' in form.errors:
            messages.error(self.request, 'O campo nome é obrigatório.')
        return self.render_to_response(self.get_context_data(form=form))


class FolderEditView(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folder/create-folder.html'

    def get_object(self, *args, **kwargs):
        object = super(FolderEditView, self).get_object(*args, **kwargs)
        if object.user != self.request.user:
            raise Http404
        return object

    def get_success_url(self):
        messages.success(self.request, 'Pasta modificada com sucesso!')
        return redirect('dashboard', pk=self.object.slug)


class FolderListView(ListView):
    model = Folder
    template_name = 'folder/folder_list.html'

    def get_context_data(self, **kwargs):
        context = super(FolderListView, self).get_context_data(**kwargs)
        context['public_folders'] = Folder.objects.filter(permission='public',
                                                          status=True).exclude(user=self.request.user).order_by('-name')
        return context

    def get_queryset(self):
        object_list = Folder.objects.filter(user=self.request.user, status=True).order_by('-name')
        return object_list


class FolderDetailView(DetailView):
    model = Folder
    template_name = 'folder/folder_detail.html'


class FileCreateView(CreateView):
    model = File
    form_class = FileForm

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(FileCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        folder = Folder.objects.get(id=self.kwargs['folder_id'])
        if folder.user == self.request.user:
            file = File()
            file.name = form.cleaned_data['name']
            file.file = form.cleaned_data['file']
            file.folder = folder
            file.status = True
            file.user = self.request.user
            file.save()
            messages.success(self.request, 'Arquivo salvo com sucesso!')
            return redirect('folder_detail', folder_id=self.kwargs['folder_id'])
        else:
            raise Http404

    def form_invalid(self, form):
        messages.error(self.request, 'Os campos com * são obrigatórios.')
        return self.render_to_response(self.get_context_data(form=form))


class FileListView(ListView):
    model = Folder
    template_name = 'file/file_list.html'

    def get_queryset(self):
        object_list = File.objects.filter(user=self.request.user, status=True).order_by('-name')
        return object_list
