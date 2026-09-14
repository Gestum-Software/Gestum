from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Resource
from .forms import ResoruceForm


class ResourcesListView(ListView):
    model = Resource


class ResourcesCreateView(CreateView):
    model = Resource
    form_class = ResoruceForm
    success_url = '/recursos/'
