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
        html = render_to_string('financier/notification_email.html', {'object': self.object})
        users = User.objects.filter(receive_email=True)
        email_list = []
        subject = u'[Extranet-Fenacon] Solicitação de reembolso de viagem de %s' % self.object.beneficiary
        for user in users:
            email_list.append(user.email)
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

    def get_success_url(self):
        messages.success(self.request, 'Solicitação modificada com sucesso!')
        return reverse('list_refund')
