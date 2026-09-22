from django.urls import path
from .views.users import (
    AccountsListView,
    AccountsWithGroupsCreateView,
    AccountsDeleteView,
)
from .views.setup import (
    InitialAdminCreateView,
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

    path(
        'create-initial-admin/',
        InitialAdminCreateView.as_view(),
        name='initial-admin-create'
    )
]
