from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
)
from ..forms import CustomUserWithGroupsCreationForm

User = get_user_model()


class AccountsListView(ListView):
    model = User
    template_name = 'accounts/accounts_list.html'


class AccountsWithGroupsCreateView(CreateView):
    model = User
    form_class = CustomUserWithGroupsCreationForm
    success_url = '/usuarios/'
    template_name = 'accounts/accounts_form_with_groups.html'


class AccountsDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('accounts:accounts_list')
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'accounts/accounts_confirm_delete.html'
