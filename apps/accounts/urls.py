from django.urls import path
from .views import (
    AccountsListView,
    AccountsCreateView,
)

app_name = 'accounts'


urlpatterns = [
    path(
        '',
        AccountsListView.as_view(),
        name='accounts_list',
    ),

    path(
        'create/',
        AccountsCreateView.as_view(),
        name='accounts_create',
    ),
]
