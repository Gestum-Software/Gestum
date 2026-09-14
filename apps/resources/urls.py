from django.urls import path
from .views import (
    ResourcesListView,
    ResourcesCreateView,
    ResourceDetailView,
    ResourceUpdateView,
    ResourceDeleteView,
)


app_name = 'resource'

urlpatterns = [
    path(
        '',
        ResourcesListView.as_view(),
        name='resource_list',
    ),

    path(
        'create/',
        ResourcesCreateView.as_view(),
        name='resource_create',
    ),

    path(
        'recurso/<str:nome>/',
        ResourceDetailView.as_view(),
        name='resource_detail',
    ),

    path(
        'update/<str:nome>',
        ResourceUpdateView.as_view(),
        name='resource_update',
    ),

    path(
        'delete/<str:nome>',
        ResourceDeleteView.as_view(),
        name='resource_delete',
    )
]
