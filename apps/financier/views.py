from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView

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
    template_name = 'financier/list_refund.html'

    @method_decorator(login_required(login_url='/'))
    def dispatch(self, *args, **kwargs):
        return super(TravelRefundListView, self).dispatch(*args, **kwargs)
