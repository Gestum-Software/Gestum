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
from .models import Resource
from .forms import ResourceForm


class ResourcesListView(LoginRequiredMixin, ListView):
    model = Resource


class ResourcesCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'
    permission_required = 'resources.add_resource'


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    slug_field = 'nome'
    slug_url_kwarg = 'nome'


class ResourceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'
    slug_field = 'nome'
    slug_url_kwarg = 'nome'
    permission_required = 'resources.change_resource'


class ResourceDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = Resource
    success_url = reverse_lazy('resource:resource_list')
    slug_field = 'nome'
    slug_url_kwarg = 'nome'
    permission_required = 'resources.delete_resource'
