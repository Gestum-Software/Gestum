from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import DetailView
from apps.core.mixins import OwnerOrPrivilegedRequiredMixin
from .models import Ticket
from .forms import TicketForm


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["show_all_actions"] = (
            user.is_superuser
            or user.groups.filter(name__in=("tecnico", "admin")).exists()
        )
        return context


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:ticket_list')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'


class TickerUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    OwnerOrPrivilegedRequiredMixin,
    UpdateView,
):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:ticket_list')
    slug_url_kwarg = 'titulo'
    slug_field = 'titulo'
    permission_required = 'tickets.change_ticket'


class TicketDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    OwnerOrPrivilegedRequiredMixin,
    DeleteView,
):
    model = Ticket
    success_url = reverse_lazy('tickets:ticket_list')
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'
    permission_required = 'tickets.delete_ticket'
