from django.urls import path
from .views import (
    ResourcesCreateView,
    ResourcesListView
)


app_name = 'resource'

urlpatterns = [
    path('', ResourcesListView.as_view(), name='resource_list'),
    path('create', ResourcesCreateView.as_view(), name='resource_create')
]
