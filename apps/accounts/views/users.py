from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView,
    DeleteView,
)
from ..forms import CustomUserWithGroupsCreationForm

User = get_user_model()


class AccountsListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    template_name = 'accounts/accounts_list.html'
    permission_required = 'accounts.view_customuser'


class AccountsWithGroupsCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView,
):
    model = User
    form_class = CustomUserWithGroupsCreationForm
    success_url = '/accounts/'
    template_name = 'accounts/accounts_form_with_groups.html'
    permission_required = 'accounts.add_customuser'


class AccountsDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView,
):
    model = User
    success_url = reverse_lazy('accounts:accounts_list')
    slug_field = 'username'
    slug_url_kwarg = 'username'
    template_name = 'accounts/accounts_confirm_delete.html'
    permission_required = 'accounts.delete_customuser'
