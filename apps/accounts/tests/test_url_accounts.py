from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from apps.accounts.views.users import (
    AccountsDeleteView,
    AccountsListView,
    AccountsWithGroupsCreateView,
)
from apps.accounts.views.setup import InitialAdminCreateView


User = get_user_model()


class AccountsUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="usuario-teste",
            password="SenhaSegura123!",
        )

    def test_account_urls_reverse_to_expected_paths(self):
        expected_urls = {
            "accounts_list": ("/usuarios/", {}),
            "accounts_create": ("/usuarios/create/", {}),
            "initial-admin-create": ("/usuarios/create-initial-admin/", {}),
            "accounts_delete": (
                f"/usuarios/delete/{self.user.username}",
                {"username": self.user.username},
            ),
        }

        for url_name, (expected_path, kwargs) in expected_urls.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    reverse(f"accounts:{url_name}", kwargs=kwargs),
                    expected_path,
                )

    def test_account_urls_resolve_to_expected_views(self):
        expected_views = {
            "accounts_list": AccountsListView,
            "accounts_create": AccountsWithGroupsCreateView,
            "initial-admin-create": InitialAdminCreateView,
            "accounts_delete": AccountsDeleteView,
        }

        for url_name, expected_view in expected_views.items():
            kwargs = (
                {}
                if url_name != "accounts_delete"
                else {"username": self.user.username}
            )

            with self.subTest(url_name=url_name):
                resolved_url = resolve(
                    reverse(f"accounts:{url_name}", kwargs=kwargs)
                )

                self.assertIs(resolved_url.func.view_class, expected_view)

    def test_account_urls_return_successful_responses(self):
        url_kwargs = {
            "accounts_list": {},
            "accounts_create": {},
            "initial-admin-create": {},
            "accounts_delete": {"username": self.user.username},
        }

        for url_name, kwargs in url_kwargs.items():
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(f"accounts:{url_name}", kwargs=kwargs)
                )

                self.assertEqual(response.status_code, 200)