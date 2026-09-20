from django.test import TestCase
from django.urls import reverse

from apps.core.views import DashboardTemplateView


class DashboardViewTest(TestCase):
    def test_home_view_renders_dashboard(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")
        self.assertContains(response, "<h1>Dahsboard</h1>", html=True)

    def test_home_url_uses_dashboard_view(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.resolver_match.url_name, "home")
        self.assertIs(
            response.resolver_match.func.view_class,
            DashboardTemplateView,
        )