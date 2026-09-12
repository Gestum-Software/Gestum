from django.views.generic.list import ListView

from .models import Resource


class ResourcesListView(ListView):
    model = Resource
