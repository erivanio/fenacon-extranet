# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, CreateView
from apps.core.forms import LoginForm, FolderForm
from apps.core.models import User, Folder


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