from django.urls import path
from .views.users import (
    AccountsListView,
    AccountsWithGroupsCreateView,
    AccountsDeleteView,
    AccountsProfileUpdateView,
)
from .views.setup import (
    InitialAdminCreateView,
)
from .views.authentication import (
    AccountsLoginView,
    AccountsLogoutView,
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
        name='accounts_initial_admin_create',
    ),

    path(
        'login/',
        AccountsLoginView.as_view(),
        name='accounts_login',
    ),

    path(
        'logout/',
        AccountsLogoutView.as_view(),
        name='accounts_logout',
    ),

    path(
        'edit-profile/',
        AccountsProfileUpdateView.as_view(),
        name='edit_profile',
    ),
]
