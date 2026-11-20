import sqlite3
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.db import connection, transaction
from django.db.utils import OperationalError
from django.db.models import F
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from ..forms import CustomUserCreationForm
from ..models import InitialAdminSetupLock

User = get_user_model()


class InitialAdminCreateView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'accounts/accounts_initial_admin_form.html'
    success_url = reverse_lazy('accounts:accounts_list')

    def dispatch(self, request, *args, **kwargs):
        if User.objects.exists():
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        retry_deadline = time.monotonic() + 5
        while True:
            try:
                with transaction.atomic():
                    lock_acquired = InitialAdminSetupLock.objects.filter(
                        pk=1
                    ).update(revision=F('revision') + 1)
                    if not lock_acquired:
                        raise RuntimeError(
                            'Initial admin setup lock is missing.'
                        )
                    if User.objects.exists():
                        raise Http404
                    return super().post(request, *args, **kwargs)
            except OperationalError as error:
                sqlite_error = error.__cause__
                error_code = getattr(sqlite_error, 'sqlite_errorcode', None)
                is_sqlite_lock_error = (
                    connection.vendor == 'sqlite'
                    and error_code is not None
                    and error_code & 0xFF
                    in (sqlite3.SQLITE_BUSY, sqlite3.SQLITE_LOCKED)
                )
                if not is_sqlite_lock_error or time.monotonic() >= retry_deadline:
                    raise
                time.sleep(0.01)

    def form_valid(self, form):
        response = super().form_valid(form)

        group = Group.objects.get(name='admin')
        self.object.groups.add(group)

        return response
