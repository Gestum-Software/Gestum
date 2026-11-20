from django.contrib.auth.mixins import LoginRequiredMixin
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


class ResourcesCreateView(LoginRequiredMixin, CreateView):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    slug_field = 'nome'
    slug_url_kwarg = 'nome'


class ResourceUpdateView(LoginRequiredMixin, UpdateView):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'
    slug_field = 'nome'
    slug_url_kwarg = 'nome'


class ResourceDeleteView(LoginRequiredMixin, DeleteView):
    model = Resource
    success_url = reverse_lazy('resource:resource_list')
    slug_field = 'nome'
    slug_url_kwarg = 'nome'
