from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


class AccountsLoginView(LoginView):
    template_name = 'accounts/accounts_login'
    redirect_authenticated_user = True
    success_url = reverse_lazy('core:home')
