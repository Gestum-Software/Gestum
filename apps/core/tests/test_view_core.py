from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from apps.core.views import DashboardTemplateView

User = get_user_model()


class DashboardViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )

        self.client.force_login(self.user)

    def test_home_view_renders_dashboard(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/dashboard.html")

    def test_home_url_uses_dashboard_view(self):
        response = self.client.get(reverse("core:home"))

        self.assertEqual(response.resolver_match.url_name, "home")
        self.assertIs(
            response.resolver_match.func.view_class,
            DashboardTemplateView,
        )
