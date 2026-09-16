from django.urls import path
from .views import (
    AccountsListView,
    AccountsWithGroupsCreateView,
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
        AccountsWithGroupsCreateView.as_view(),
        name='accounts_create',
    ),
]
