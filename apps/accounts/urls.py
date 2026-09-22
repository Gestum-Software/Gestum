from django.urls import path
from .views.users import (
    AccountsListView,
    AccountsWithGroupsCreateView,
    AccountsDeleteView,
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

    path(
        'delete/<str:username>',
        AccountsDeleteView.as_view(),
        name='accounts_delete',
    ),
]
