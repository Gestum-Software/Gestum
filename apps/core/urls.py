from django.urls import path
from .views import BaseTemplateViewView

app_name = 'core'

urlpatterns = [
    path('', BaseTemplateViewView.as_view(), name="home"),
]