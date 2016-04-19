# -*- coding: utf-8 -*-
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from apps.core.models import User

from apps.financier.forms import TravelRefundForm
from apps.financier.models import TravelRefund


class TravelRefundCreateView(CreateView):
    model = TravelRefund
    form_class = TravelRefundForm
    template_name = 'financier/create_refund.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(TravelRefundCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.save()
        users = User.objects.filter(receive_email=True)
        email_list = []
        text = ''
        subject = u'[Extranet-Fenacon]'
        if self.object.status == '1':
            text = u'Nova solicitação de reembolso'
            subject = u'[Extranet-Fenacon] %s de %s' % (text, self.object.beneficiary)
            for user in users:
                email_list.append(user.email)
        elif self.object.status == '2' or self.object.status == '4':
            text = u'Alteração no estado da solicitação de reembolso'
            subject = u'[Extranet-Fenacon] %s de %s' % (text, self.object.beneficiary)
            for user in users:
                email_list.append(user.email)
            email_list.append(self.object.beneficiary.email)
        elif self.object.status == '3':
            text = u'Solicitação de reembolso paga'
            subject = u'[Extranet-Fenacon] %s' % text
            email_list.append(self.object.beneficiary.email)
        html = render_to_string('financier/notification_email.html', {'object': self.object, 'text': text})
        mail = EmailMultiAlternatives(subject, '', '', email_list)
        mail.attach_alternative(html, 'text/html')
        mail.send()

        return HttpResponseRedirect(self.get_success_url())


    def get_success_url(self):
        messages.success(self.request, 'Solicitação modificada com sucesso!')
        return reverse('list_refund')


class TravelRefundListView(ListView):
    model = TravelRefund
    template_name = 'financier/list-refund.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(TravelRefundListView, self).dispatch(*args, **kwargs)


class TravelRefundUpdateView(UpdateView):
    model = TravelRefund
    form_class = TravelRefundForm
    template_name = 'financier/create_refund.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'status' in form.changed_data and self.object.status == '2':
            self.object.approved_by = self.request.user
        self.object.save()
        users = User.objects.filter(receive_email=True)
        email_list = []
        text = ''
        subject = u'[Extranet-Fenacon]'
        if self.object.status == '1':
            text = u'Nova solicitação de reembolso'
            subject = u'[Extranet-Fenacon] %s de %s' % (text, self.object.beneficiary)
            for user in users:
                email_list.append(user.email)
        elif self.object.status == '2' or self.object.status == '4':
            text = u'Alteração no estado da solicitação de reembolso'
            subject = u'[Extranet-Fenacon] %s de %s' % (text, self.object.beneficiary)
            for user in users:
                email_list.append(user.email)
            email_list.append(self.object.beneficiary.email)
        elif self.object.status == '3':
            text = u'Solicitação de reembolso paga'
            subject = u'[Extranet-Fenacon] %s' % text
            email_list.append(self.object.beneficiary.email)
        html = render_to_string('financier/notification_email.html', {'object': self.object, 'text': text})
        mail = EmailMultiAlternatives(subject, '', '', email_list)
        mail.attach_alternative(html, 'text/html')
        mail.send()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        messages.success(self.request, 'Solicitação modificada com sucesso!')
        return reverse('list_refund')
