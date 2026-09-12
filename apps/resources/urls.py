from django.urls import path
from .views import ResourcesListView


app_name = 'resource'

urlpatterns = [
    path('', ResourcesListView.as_view(), name="home"),
]
