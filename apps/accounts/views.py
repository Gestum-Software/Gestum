from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import (
    CreateView,
    UpdateView,
    DeleteView,
)
from .forms import CustomUserWithGroupsCreationForm

User = get_user_model()


class AccountsListView(ListView):
    model = User


class AccountsWithGroupsCreateView(CreateView):
    model = User
    form_class = CustomUserWithGroupsCreationForm
    success_url = '/usuarios/'
