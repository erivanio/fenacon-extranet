# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Q
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_protect
from django.utils.translation import ugettext as _
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import redirect, resolve_url
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, DetailView, CreateView, UpdateView, DeleteView, ListView
from apps.core.forms import LoginForm, UserEditForm, UserCreateForm, AreaForm, FolderForm, GroupCreateForm, FileForm, \
    InformativeForm
from apps.core.models import User, Folder, File, Area, Group, History, Informative


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
        next_page = request.POST.get('next')
        if form.is_valid():
            if request.POST.has_key('remember_me'):
                request.session.set_expiry(29030400)
            u = authenticate(username=form.cleaned_data['name'], password=form.cleaned_data['password'])
            if u is not None:
                if u.is_active:
                    login(request, u)
                    if next_page:
                        return HttpResponseRedirect(next_page)
                    else:
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(GroupCreateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupCreateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()

        return context

    def get_success_url(self):
        messages.success(self.request, 'Grupo criado com sucesso!')
        return reverse('create_group')


class GroupUpdateView(UpdateView):
    model = Group
    form_class = GroupCreateForm
    template_name = 'user/group_create.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(GroupUpdateView, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(GroupUpdateView, self).get_context_data(**kwargs)
        context['groups'] = Group.objects.all()

        return context

    def get_success_url(self):
        messages.success(self.request, 'Grupo editado com sucesso!')
        return reverse('update_group')


class UserListView(ListView):
    model = User
    template_name = 'user/list-user.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(UserListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        q = self.request.GET.get('q')
        object_list = User.objects.all()
        if q:
            object_list = object_list.filter(Q(first_name__icontains=q) |
                                             Q(username__icontains=q) |
                                             Q(last_name__icontains=q) |
                                             Q(email__icontains=q) |
                                             Q(job__icontains=q))

        return object_list

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = 'user/user_create.html'

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(UserCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        history = History()
        history.user = self.request.user
        history.created_at = datetime.now()
        history.icon = 'fa-user'
        history.content = '<a href="%s">%s</a> adicionou a conta <a href="%s">%s</a>' % (self.request.user.get_absolute_url(), self.request.user.get_display_name(), self.object.get_absolute_url(), self.object.get_display_name())
        history.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Usuário criado com sucesso!')
        return reverse('create_user')


class UserEditView(UpdateView):
    model = User
    form_class = UserEditForm
    template_name = 'user/user_edit.html'

    def get_object(self, *args, **kwargs):
        obj = super(UserEditView, self).get_object(*args, **kwargs)
        if obj != self.request.user and not self.request.user.is_superuser:
            raise Http404
        return obj

    def form_valid(self, form):
        if not self.request.user.is_superuser:
            superuser_fields = ['is_active', 'is_superuser', 'groups', 'areas_read',
                                'receive_email', 'permissions', 'expirated_date']
            for field in superuser_fields:
                if field in form.changed_data:
                    raise Http404
        form.save()
        history = History()
        history.user = self.request.user
        history.created_at = datetime.now()
        history.icon = 'fa-user'
        if self.request.user != self.object:
            history.content = '<a href="%s">%s</a> editou o perfil de <a href="%s">%s</a>' % (self.request.user.get_absolute_url(), self.request.user.get_display_name(), self.object.get_absolute_url(), self.object.get_display_name())
        else:
            history.content = '<a href="%s">%s</a> editou seu perfil' % (self.request.user.get_absolute_url(), self.request.user.get_display_name())
        history.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Perfil modificado com sucesso!')
        return reverse('edit_user', kwargs={'slug': self.object.slug})


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
            context['folders'] = Folder.objects.filter(name__icontains=q,
                                                       parent__isnull=True, status=True).order_by('-name')
            context['files'] = File.objects.filter(name__icontains=q,
                                                   folder__isnull=True, status=True).order_by('-name')
        else:
            context['informatives'] = Informative.objects.filter(status=True).order_by('-created_at')[:3]
            context['folders'] = Folder.objects.filter(user__slug=self.kwargs['slug'],
                                                       parent__isnull=True, status=True).order_by('-name')
            context['files'] = File.objects.filter(user__slug=self.kwargs['slug'],
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
        context['folders'] = Folder.objects.filter(status=False).order_by('-name')
        context['files'] = File.objects.filter(status=False).order_by('-name')

        return context


class FolderUpdateView(UpdateView):
    model = Folder
    form_class = FolderForm
    template_name = 'folder/update-folder.html'

    def get_object(self, *args, **kwargs):
        obj = super(FolderUpdateView, self).get_object(*args, **kwargs)
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        form.save_m2m()
        history = History()
        history.user = self.request.user
        history.created_at = datetime.now()
        history.icon = 'fa-folder'
        history.content = '<a href="%s">%s</a> editou a pasta <a href="%s">%s</a>' % (self.request.user.get_absolute_url(), self.request.user.get_display_name(), self.object.get_absolute_url(), self.object.name)
        history.save()

        return HttpResponseRedirect(self.get_success_url())

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


class FolderShareView(DetailView):
    model = Folder
    template_name = 'share.html'

    def get_object(self, *args, **kwargs):
        obj = super(FolderShareView, self).get_object(*args, **kwargs)
        if not obj.status_link:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super(FolderShareView, self).get_context_data(**kwargs)
        context['folders'] = Folder.objects.filter(parent=kwargs['object'], status=True).order_by('-name')
        context['files'] = File.objects.filter(folder=kwargs['object'], status=True).order_by('-name')

        return context


class FileShareView(DetailView):
    model = File
    template_name = 'share.html'

    def get_object(self, *args, **kwargs):
        obj = super(FileShareView, self).get_object(*args, **kwargs)
        if not obj.status_link:
            raise Http404
        return obj

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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
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

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super(AreaUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Área modificada com sucesso!')
        return reverse('detail_area', kwargs={'slug': self.object.slug, 'pk': self.object.pk})


class AreaDeleteView(DeleteView):
    model = Area

    def get_object(self, queryset=None):
        obj = super(AreaDeleteView, self).get_object()
        for folder in obj.folder_set.all():
            folder.delete()
        for file in obj.file_set.all():
            file.delete()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Área deletada com sucesso!')
        return reverse('dashboard', kwargs={'slug': self.request.user.slug})


class InformativeCreateView(CreateView):
    model = Informative
    form_class = InformativeForm
    template_name = 'informative/informative_form.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(InformativeCreateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Informativo criado com sucesso!')
        return reverse('list_informative')

    def form_valid(self, form):
        informative = Informative()
        informative.title = form.cleaned_data['title']
        informative.content = form.cleaned_data['content']
        informative.status = form.cleaned_data['status']
        informative.user = self.request.user
        informative.save()
        return HttpResponseRedirect(self.get_success_url())


class InformativeUpdateView(UpdateView):
    model = Informative
    form_class = InformativeForm
    template_name = 'informative/informative_form.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(InformativeUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, 'Informativo modificado com sucesso!')
        return reverse('list_informative')


class InformativeListView(ListView):
    model = Informative
    template_name = 'informative/informative_list.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(InformativeListView, self).dispatch(*args, **kwargs)


class InformativeDeleteView(DeleteView):
    model = Informative

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(InformativeDeleteView, self).dispatch(*args, **kwargs)

    def get_object(self, queryset=None):
        obj = super(InformativeDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Informativo deletado com sucesso!')
        return reverse('list_informative')


class FolderDeleteView(DeleteView):
    model = Folder

    def get_object(self, queryset=None):
        obj = super(FolderDeleteView, self).get_object()
        for folder in obj.children.all():
            folder.delete()
        for file in obj.file_set.all():
            file.delete()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Pasta deletada com sucesso!')
        return u'/%s/lixeira/' % self.request.user.slug


class UserDeleteView(DeleteView):
    model = User

    def get_object(self, queryset=None):
        obj = super(UserDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Usuário deletado com sucesso!')
        return reverse('list_user')


class FileUpdateView(UpdateView):
    model = File
    form_class = FileForm
    template_name = 'folder/update-file.html'

    def get_object(self, *args, **kwargs):
        obj = super(FileUpdateView, self).get_object(*args, **kwargs)
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        history = History()
        history.user = self.request.user
        history.created_at = datetime.now()
        history.icon = 'fa-file'
        history.content = '<a href="%s">%s</a> renomeou o arquivo "%s"' % (self.request.user.get_absolute_url(), self.request.user.get_display_name(), self.object.name)
        history.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Arquivo modificada com sucesso!')
        if self.object.folder:
            return reverse('detail_folder', kwargs={'slug': self.object.folder.slug, 'pk': self.object.folder.pk})
        elif self.object.area:
            return reverse('detail_area', kwargs={'slug': self.object.area.slug, 'pk': self.object.area.pk})
        else:
            return reverse('dashboard', kwargs={'slug': self.object.user.slug})


class FileDeleteView(DeleteView):
    model = File

    def get_object(self, queryset=None):
        obj = super(FileDeleteView, self).get_object()
        return obj

    def get_success_url(self):
        messages.success(self.request, 'Arquivo deletado com sucesso!')
        return u'/%s/lixeira/' % self.request.user.slug


class HistoryListView(ListView):
    model = History
    template_name = 'history.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(HistoryListView, self).dispatch(*args, **kwargs)


class MyActionsListView(ListView):
    model = History
    template_name = 'history.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(MyActionsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        object_list = History.objects.filter(user=self.request.user)
        return object_list


class UserActionsListView(ListView):
    model = History
    template_name = 'history.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(UserActionsListView, self).dispatch(*args, **kwargs)

    def get_queryset(self):
        object_list = History.objects.filter(user__slug=self.kwargs['slug'])
        return object_list


def create_folder(request):
    if request.method == 'POST':
        folder = Folder()
        folder.name = request.POST.get('name')
        folder.permission = request.POST.get('permission')
        folder.user = request.user
        if request.POST.get('parent'):
            parent = Folder.objects.get(id=int(request.POST.get('parent')))
            if not request.user in parent.users_read.all():
                folder.parent = parent
                folder.save()
                history = History()
                history.user = request.user
                history.created_at = datetime.now()
                history.icon = 'fa-folder'
                history.content = '<a href="%s">%s</a> adicionou a pasta "%s" na pasta <a href="%s">%s</a>' % (folder.user.get_absolute_url(), folder.user.get_display_name(), folder.name, parent.get_absolute_url(), parent.name)
                history.save()
                messages.success(request, 'Pasta criada com sucesso!')
            else:
                messages.warning(request, 'Você não possui permissão de escrita nesta pasta')
            return reverse('detail_folder', request, kwargs={'slug': parent.slug, 'pk': parent.pk})
        elif request.POST.get('area'):
            area = Area.objects.get(id=int(request.POST.get('area')))
            if area in request.user.areas.all() or request.user.is_superuser:
                folder.area = area
                folder.save()
                history = History()
                history.user = request.user
                history.created_at = datetime.now()
                history.icon = 'fa-folder'
                history.content = '<a href="%s">%s</a> adicionou a pasta "%s" em <a href="%s">%s</a>' % (folder.user.get_absolute_url(), folder.user.get_display_name(), folder.name, area.get_absolute_url(), area.name)
                history.save()
                messages.success(request, 'Pasta criada com sucesso!')
            else:
                messages.warning(request, 'Você não possui permissão de escrita nesta área')
            return redirect(reverse('detail_area',request, kwargs={'slug': area.slug, 'pk': area.pk}))
        else:
            folder.save()
            history = History()
            history.user = request.user
            history.created_at = datetime.now()
            history.icon = 'fa-folder'
            history.content = '<a href="%s">%s</a> adicionou a pasta "%s"' % (folder.user.get_absolute_url(), folder.user.get_display_name(), folder.name)
            history.save()
            messages.success(request, 'Pasta criada com sucesso!')
            return reverse('dashboard', request, kwargs={'slug': request.user.slug})


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
            history = History()
            history.user = request.user
            history.created_at = datetime.now()
            history.icon = 'fa-file'
            history.content = '<a href="%s">%s</a> adicionou o arquivo "%s" a pasta <a href="%s">%s</a>' % (file.user.get_absolute_url(), file.user.get_display_name(), file.name, folder.get_absolute_url(), folder.name)
            history.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return reverse('detail_folder', request, kwargs={'slug': folder.slug, 'pk': folder.pk})
        elif request.POST.get('area'):
            area = Area.objects.get(id=int(request.POST.get('area')))
            if area in request.user.areas.all() or request.user.is_superuser:
                file.area = area
                file.save()
                history = History()
                history.user = request.user
                history.created_at = datetime.now()
                history.icon = 'fa-file'
                history.content = '<a href="%s">%s</a> adicionou o arquivo "%s" em <a href="%s">%s</a>' % (file.user.get_absolute_url(), file.user.get_display_name(), file.name, area.get_absolute_url(), area.name)
                history.save()
                messages.success(request, 'Arquivo adicionado com sucesso!')
            else:
                messages.warning(request, 'Você não possui permissão de escrita nesta área')
            return reverse('detail_area', request, kwargs={'slug': area.slug, 'pk': area.pk})
        else:
            file.save()
            history = History()
            history.user = request.user
            history.created_at = datetime.now()
            history.icon = 'fa-file'
            history.content = '<a href="%s">%s</a> adicionou o arquivo "%s"' % (file.user.get_absolute_url(), file.user.get_display_name(), file.name)
            history.save()
            messages.success(request, 'Arquivo adicionado com sucesso!')
            return reverse('dashboard', request, kwargs={'slug': request.user.slug})


class PasswordResetUnregister(TemplateView):
    template_name = 'registration/password_reset_unregister.html'


@csrf_protect
def password_reset(request, is_admin_site=False,
                   template_name='registration/password_reset_form.html',
                   email_template_name='registration/password_reset_email.html',
                   subject_template_name='registration/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None):
    if post_reset_redirect is None:
        try:
            if User.objects.filter(email=request.POST['email']).exists():
                post_reset_redirect = reverse('password_reset_done')
            else:
                return redirect('password_reset_unregister')
        except:
            post_reset_redirect = reverse('password_reset_done')
    else:
        post_reset_redirect = resolve_url(post_reset_redirect)
    if request.method == "POST":
        form = password_reset_form(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': token_generator,
                'from_email': from_email,
                'email_template_name': email_template_name,
                'subject_template_name': subject_template_name,
                'request': request,
                'html_email_template_name': html_email_template_name,
            }
            if is_admin_site:
                opts = dict(opts, domain_override=request.get_host())
            form.save(**opts)
            return HttpResponseRedirect(post_reset_redirect)
    else:
        form = password_reset_form()
    context = {
        'form': form,
        'title': _('Password reset'),
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)