from django.views.generic import TemplateView


class DashboardTemplateView(TemplateView):
    template_name = 'core/dashboard.html'
