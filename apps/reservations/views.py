from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from apps.core.mixins import OwnerOrPrivilegedRequiredMixin
from .forms import ReservationForm
from .models import Reservation


class ReservationListView(LoginRequiredMixin, ListView):
    model = Reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        context["show_all_actions"] = (
            user.is_superuser
            or user.groups.filter(name__in=("tecnico", "admin")).exists()
        )
        return context


class ReservationCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Reservation
    form_class = ReservationForm
    success_url = '/reservas/'
    permission_required = 'reservations.add_reservation'

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)


class ReservationDetailView(LoginRequiredMixin, DetailView):
    model = Reservation
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'


class ReservationUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    OwnerOrPrivilegedRequiredMixin,
    UpdateView,
):
    model = Reservation
    form_class = ReservationForm
    success_url = '/reservas/'
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'
    permission_required = 'reservations.change_reservation'


class ReservationDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    OwnerOrPrivilegedRequiredMixin,
    DeleteView,
):
    model = Reservation
    success_url = reverse_lazy('reservations:reservation_list')
    slug_field = 'titulo'
    slug_url_kwarg = 'titulo'
    permission_required = 'reservations.delete_reservation'
