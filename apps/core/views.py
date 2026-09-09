from django.shortcuts import render
from django.views.generic import TemplateView


class BaseTemplateView(TemplateView):
    template_name = 'core/base.html'
