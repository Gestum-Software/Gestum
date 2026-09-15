from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import ReservationForm
from .models import Reservation


class ReservationListView(ListView):
    model = Reservation


class ReservationCreateView(CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = '/reservas/'


class ReservationDetailView(DetailView):
    model = Reservation
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'
