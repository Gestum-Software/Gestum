from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from ..forms import CustomUserCreationForm

User = get_user_model()


class InitialAdminCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/accounts_initial_admin_form.html'
    success_url = reverse_lazy('accounts:accounts_list')

    def form_valid(self, form):
        response = super().form_valid(form)

        group = Group.objects.get(name='admin')
        self.object.groups.add(group)

        return response
