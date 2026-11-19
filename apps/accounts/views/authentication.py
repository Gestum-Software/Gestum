from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class AccountsLoginView(LoginView):
    template_name = 'accounts/accounts_login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')


class AccountsLogoutView(LoginRequiredMixin, LogoutView):
    pass
