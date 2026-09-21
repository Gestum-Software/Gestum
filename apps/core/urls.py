from django.urls import path
from .views import DashboardTemplateView

app_name = 'core'

urlpatterns = [
    path('', DashboardTemplateView.as_view(), name="home"),
]
