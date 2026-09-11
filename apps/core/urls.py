from django.urls import path
from .views import BaseTemplateView

app_name = 'core'

urlpatterns = [
    path('', BaseTemplateView.as_view(), name="home"),
]
