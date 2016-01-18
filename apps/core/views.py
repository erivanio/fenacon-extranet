# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from apps.core.forms import LoginForm


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
                    return redirect('dashboard')
            messages.error(self.request, 'Email ou senha inválidos')

        return redirect('login')


class LogoutView(TemplateView):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')
