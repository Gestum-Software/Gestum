from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views.generic.detail import DetailView
from .models import Ticket
from .forms import TicketForm


class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket


class TicketCreateView(LoginRequiredMixin, CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:ticket_list')


class TicketDetailView(LoginRequiredMixin, DetailView):
    model = Ticket
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'


class TickerUpdateView(LoginRequiredMixin, UpdateView):
    model = Ticket
    form_class = TicketForm
    success_url = reverse_lazy('tickets:ticket_list')
    slug_url_kwarg = 'titulo'
    slug_field = 'titulo'


class TicketDeleteView(LoginRequiredMixin, DeleteView):
    model = Ticket
    success_url = reverse_lazy('tickets:ticket_list')
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'
