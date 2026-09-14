from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from .models import Resource
from .forms import ResourceForm


class ResourcesListView(ListView):
    model = Resource


class ResourcesCreateView(CreateView):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'


class ResourceDetailView(DetailView):
    model = Resource
    slug_field = 'nome'
    slug_url_kwarg = 'nome'


class ResourceUpdateView(UpdateView):
    model = Resource
    form_class = ResourceForm
    success_url = '/recursos/'
    slug_field = 'nome'
    slug_url_kwarg = 'nome'
