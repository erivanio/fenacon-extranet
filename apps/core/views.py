# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView
from apps.core.forms import LoginForm, UserEditForm, UserCreateForm, AreaForm, FolderForm, GroupCreateForm
from apps.core.models import User, Folder, File, Area, Group


class LoginView(TemplateView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('dashboard', slug=request.user.slug)
        return super(LoginView, self).dispatch(request, *args, **kwargs)

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
        return redirect('login')


class GroupCreateView(CreateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'user/group_create.html'

    def get_success_url(self):
        messages.success(self.request, 'Grupo criado com sucesso!')
        return reverse('create_group')


class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/user_create.html'

    def get_success_url(self):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return reverse('create_user')


class UserEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user/user_edit.html'

    def get_object(self, *args, **kwargs):
        obj = super(UserEditView, self).get_object(*args, **kwargs)
        if obj != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Perfil modificado com sucesso!')
        return reverse('edit_user', kwargs={'slug': self.request.user.slug})


class DashboardDetailView(DetailView):
    model = User
    template_name = 'dashboard.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(DashboardDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DashboardDetailView, self).get_context_data(**kwargs)
        if self.request.GET.get('q'):
            q = self.request.GET.get('q')
            context['folders'] = Folder.objects.filter(user=self.request.user, name__icontains=q,
                                                       parent__isnull=True, status=True).order_by('-name')
            context['files'] = File.objects.filter(user=self.request.user, name__icontains=q,
                                                   folder__isnull=True, status=True).order_by('-name')
        else:
            context['folders'] = Folder.objects.filter(user=self.request.user,
                                                       parent__isnull=True, status=True).order_by('-name')
            context['files'] = File.objects.filter(user=self.request.user,
                                                   folder__isnull=True, status=True).order_by('-name')

        return context


class GarbageDetailView(DetailView):
    model = User
    template_name = 'deleted_files.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(GarbageDetailView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GarbageDetailView, self).get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(user=self.request.user, status=False).order_by('-name')
        context['files'] = File.objects.filter(user=self.request.user, status=False).order_by('-name')

        return context


class FolderUpdateView(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folder/update-folder.html'

    def get_object(self, *args, **kwargs):
        obj = super(FolderUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Pasta modificada com sucesso!')
        return reverse('detail_folder', kwargs={'slug': self.object.slug, 'pk': self.object.pk})


class FolderDetailView(DetailView):
    model = Folder
    template_name = 'folder/list-folder.html'

    def get_context_data(self, **kwargs):
        context = super(FolderDetailView, self).get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(parent=kwargs['object'], status=True).order_by('-name')
        context['files'] = File.objects.filter(folder=kwargs['object'], status=True).order_by('-name')

        return context


class AreaDetailView(DetailView):
    model = Area
    template_name = 'area/detail_area.html'

    def get_context_data(self, **kwargs):
        context = super(AreaDetailView, self).get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(area=kwargs['object'], status=True).order_by('-name')
        context['files'] = File.objects.filter(area=kwargs['object'], status=True).order_by('-name')

        return context


class AreaCreateView(CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/create-area.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(AreaCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Área criada com sucesso!')
        return reverse('create_area')

    def form_valid(self, form):
        area = Area()
        area.name = form.cleaned_data['name']
        area.status = True
        area.user = self.request.user
        area.save()
        return HttpResponseRedirect(self.get_success_url())


class AreaUpdateView(UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/create-area.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(AreaUpdateView, self).dispatch(*args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(AreaUpdateView, self).get_object(*args, **kwargs)
        if obj.user != self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Área modificada com sucesso!')
        return reverse('detail_area', kwargs={'slug': self.object.slug, 'pk': self.object.pk})


class FolderDeleteView(DeleteView):
    model = Folder

    def get_object(self, queryset=None):
        obj = super(FolderDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        for folder in obj.children.all():
            folder.delete()
        for file in obj.file_set.all():
            file.delete()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Pasta deletada com sucesso!')
        return u'/%s/lixeira/' % self.request.user.slug


class FileDeleteView(DeleteView):
    model = File

    def get_object(self, queryset=None):
        obj = super(FileDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Arquivo deletado com sucesso!')
        return u'/%s/lixeira/' % self.request.user.slug


def create_folder(request):
    if request.method == 'POST':
        folder = Folder()
        folder.name = request.POST.get('name')
        folder.permission = request.POST.get('permission')
        folder.user = request.user
        if request.POST.get('parent'):
            parent = Folder.objects.get(id=int(request.POST.get('parent')))
            folder.parent = parent
            folder.save()
            messages.success(request, 'Pasta criada com sucesso!')
            return reverse('detail_folder', kwargs={'slug': parent.slug, 'pk': parent.pk})
        elif request.POST.get('area'):
            area = Area.objects.get(id=int(request.POST.get('area')))
            folder.area = area
            folder.save()
            messages.success(request, 'Pasta criada com sucesso!')
            return redirect(reverse('detail_area', kwargs={'slug': area.slug, 'pk': area.pk}))
        else:
            folder.save()
            messages.success(request, 'Pasta criada com sucesso!')
            return reverse('dashboard', kwargs={'slug': request.user.slug})


def create_file(request):
    if request.method == 'POST':
        file = File()
        file.name = request.POST.get('name')
        file.file = request.FILES.get('file')
        file.user = request.user
        if request.POST.get('folder'):
            folder = Folder.objects.get(id=int(request.POST.get('folder')))
            file.folder = folder
            file.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return reverse('detail_folder', kwargs={'slug': folder.slug, 'pk': folder.pk})
        elif request.POST.get('area'):
            area = Area.objects.get(id=int(request.POST.get('area')))
            file.area = area
            file.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return reverse('detail_area', kwargs={'slug': area.slug, 'pk': area.pk})
        else:
            file.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return reverse('dashboard', kwargs={'slug': request.user.slug})

