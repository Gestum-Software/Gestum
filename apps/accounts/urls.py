from django.urls import path
from .views import (
    AccountsListView,
)

app_name = 'accounts'


urlpatterns = [
    path(
        '',
        AccountsListView.as_view(),
        name='accounts_list',
    ),
]
