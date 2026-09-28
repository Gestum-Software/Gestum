from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AccountsLoginView(LoginView):
    template_name = 'accounts/accounts_login.html'
    redirect_authenticated_user = True
    next_page = reverse_lazy('core:home')
