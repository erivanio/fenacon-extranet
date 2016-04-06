# -*- coding: utf-8 -*-
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, UpdateView
from apps.core.models import History

from apps.financier.forms import TravelRefundForm
from apps.financier.models import TravelRefund


class TravelRefundCreateView(CreateView):
    model = TravelRefund
    form_class = TravelRefundForm
    template_name = 'financier/create_refund.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(TravelRefundCreateView, self).dispatch(*args, **kwargs)


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
