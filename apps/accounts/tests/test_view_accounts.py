from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.db import close_old_connections
from django.test import Client, TestCase, TransactionTestCase, override_settings
from django.urls import reverse

from apps.accounts.views.authentication import AccountsLoginView
from apps.accounts.views.setup import InitialAdminCreateView


User = get_user_model()

ACCOUNT_TEMPLATES = {
    "accounts/accounts_list.html": "{{ object_list }}",
    "accounts/accounts_form_with_groups.html": "{{ form }}",
    "accounts/accounts_confirm_delete.html": "{{ object }}",
    "accounts/accounts_initial_admin_form.html": "{{ form }}",
    "accounts/accounts_login.html": "{{ form }}",
    "accounts/customuser_form.html": "{{ form }}",
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": False,
        "OPTIONS": {
            "loaders": [
                (
                    "django.template.loaders.locmem.Loader",
                    ACCOUNT_TEMPLATES,
                ),
            ],
        },
    },
]

ACCOUNT_PERMISSIONS = (
    "view_customuser",
    "add_customuser",
    "delete_customuser",
)


def get_account_permissions():
    return {
        f"accounts.{codename}": Permission.objects.get(
            content_type__app_label="accounts",
            codename=codename,
        )
        for codename in ACCOUNT_PERMISSIONS
    }


@override_settings(TEMPLATES=TEMPLATES)
class AccountsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.permissions = get_account_permissions()
        cls.group = Group.objects.create(name="Administradores")
        cls.admin_group, _ = Group.objects.get_or_create(name="admin")
        cls.user = User.objects.create_user(
            username="usuario-teste",
            password="SenhaSegura123!",
        )
        cls.user.user_permissions.add(*cls.permissions.values())
        cls.user.groups.add(cls.group)

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_view_returns_accounts(self):
        response = self.client.get(reverse("accounts:accounts_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_list.html",
        )
        self.assertIn(self.user, response.context["object_list"])

    def test_login_view_get_displays_form(self):
        self.client.logout()
        response = self.client.get(reverse("accounts:accounts_login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_login.html",
        )
        self.assertIsInstance(response.context["view"], AccountsLoginView)
        self.assertEqual(response.context["form"].initial, {})

    def test_login_view_post_authenticates_user_and_redirects(self):
        self.client.logout()
        response = self.client.post(
            reverse("accounts:accounts_login"),
            data={
                "username": self.user.username,
                "password": "SenhaSegura123!",
            },
        )

        self.assertRedirects(
            response,
            reverse("core:home"),
            fetch_redirect_response=False,
        )
        self.assertEqual(int(self.client.session["_auth_user_id"]), self.user.pk)

    def test_logout_view_post_logs_out_user_and_redirects(self):
        self.client.force_login(self.user)

        response = self.client.post(reverse("accounts:accounts_logout"))

        self.assertRedirects(
            response,
            reverse("accounts:accounts_login"),
            fetch_redirect_response=False,
        )
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_view_requires_authenticated_user(self):
        self.client.logout()
        response = self.client.post(reverse("accounts:accounts_logout"))

        self.assertRedirects(
            response,
            f"{reverse('accounts:accounts_login')}?next="
            f"{reverse('accounts:accounts_logout')}",
            fetch_redirect_response=False,
        )

    def test_protected_views_require_authenticated_user(self):
        self.client.logout()
        protected_paths = (
            reverse("accounts:accounts_list"),
            reverse("accounts:accounts_create"),
            reverse("accounts:edit_profile"),
            reverse(
                "accounts:accounts_delete",
                kwargs={"username": self.user.username},
            ),
        )
        for path in protected_paths:
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertRedirects(
                    response,
                    f"{reverse('accounts:accounts_login')}?next={path}",
                    fetch_redirect_response=False,
                )

    def test_profile_update_view_get_displays_current_user_form(self):
        response = self.client.get(reverse("accounts:edit_profile"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/customuser_form.html",
        )
        self.assertEqual(response.context["form"].instance, self.user)

    def test_profile_update_view_post_updates_current_user_and_redirects(self):
        response = self.client.post(
            reverse("accounts:edit_profile"),
            data={"username": "perfil-atualizado"},
        )

        self.user.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("core:home"),
            fetch_redirect_response=False,
        )
        self.assertEqual(self.user.username, "perfil-atualizado")

    def test_profile_update_view_rejects_invalid_username(self):
        response = self.client.post(
            reverse("accounts:edit_profile"),
            data={"username": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("username", response.context["form"].errors)
        self.assertEqual(self.user.username, "usuario-teste")

    def test_protected_views_require_their_specific_permissions(self):
        protected_views = (
            (
                "accounts_list",
                {},
                "accounts.view_customuser",
            ),
            (
                "accounts_create",
                {},
                "accounts.add_customuser",
            ),
            (
                "accounts_delete",
                {"username": self.user.username},
                "accounts.delete_customuser",
            ),
        )

        for url_name, kwargs, required_permission in protected_views:
            with self.subTest(url_name=url_name):
                user = User.objects.create_user(
                    username=f"sem-{url_name}",
                    password="SenhaSegura123!",
                )
                user.user_permissions.add(
                    *(
                        permission
                        for permission_name, permission
                        in self.permissions.items()
                        if permission_name != required_permission
                    )
                )
                self.client.force_login(user)

                response = self.client.get(
                    reverse(f"accounts:{url_name}", kwargs=kwargs)
                )

                self.assertEqual(response.status_code, 403)

    def test_create_view_get_displays_form(self):
        response = self.client.get(reverse("accounts:accounts_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_form_with_groups.html",
        )
        self.assertEqual(
            response.context["form"].instance.__class__,
            User,
        )
        self.assertIsNone(response.context["form"].instance.pk)

    def test_create_view_post_creates_account_and_redirects(self):
        account_data = {
            "username": "novo-usuario",
            "password": "OutraSenha123!",
            "password1": "OutraSenha123!",
            "password2": "OutraSenha123!",
            "groups": str(self.group.pk),
        }

        response = self.client.post(
            reverse("accounts:accounts_create"),
            data=account_data,
        )

        created_user = User.objects.get(username=account_data["username"])

        self.assertRedirects(
            response,
            reverse("accounts:accounts_list"),
        )
        self.assertTrue(
            created_user.groups.filter(pk=self.group.pk).exists()
        )
        self.assertTrue(
            created_user.check_password(account_data["password1"])
        )

    def test_create_view_post_with_invalid_data_does_not_create_account(self):
        response = self.client.post(
            reverse("accounts:accounts_create"),
            data={
                "username": "",
                "password1": "",
                "password2": "",
                "groups": [],
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_form_with_groups.html",
        )
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(User.objects.count(), 1)

    def test_initial_admin_view_get_displays_form(self):
        self.user.delete()
        self.client.logout()

        response = self.client.get(
            reverse("accounts:accounts_initial_admin_create")
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_initial_admin_form.html",
        )
        self.assertIsInstance(response.context["view"], InitialAdminCreateView)
        self.assertEqual(
            response.context["form"].instance.__class__,
            User,
        )
        self.assertIsNone(response.context["form"].instance.pk)

    def test_initial_admin_view_post_creates_admin_and_redirects(self):
        self.user.delete()
        self.client.logout()
        account_data = {
            "username": "administrador-inicial",
            "password": "SenhaSegura123!",
            "password1": "SenhaSegura123!",
            "password2": "SenhaSegura123!",
        }

        response = self.client.post(
            reverse("accounts:accounts_initial_admin_create"),
            data=account_data,
        )

        created_user = User.objects.get(
            username=account_data["username"]
        )

        self.assertRedirects(
            response,
            reverse("accounts:accounts_list"),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            created_user.groups.filter(pk=self.admin_group.pk).exists()
        )
        self.assertTrue(
            created_user.check_password(account_data["password1"])
        )

    def test_initial_admin_view_post_with_invalid_data_does_not_create_account(
        self,
    ):
        self.user.delete()
        self.client.logout()

        response = self.client.post(
            reverse("accounts:accounts_initial_admin_create"),
            data={
                "username": "",
                "password1": "",
                "password2": "",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_initial_admin_form.html",
        )
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(User.objects.count(), 0)

    def test_initial_admin_view_is_not_accessible_after_setup(self):
        self.user.groups.add(self.admin_group)
        path = reverse("accounts:accounts_initial_admin_create")

        get_response = self.client.get(path)
        post_response = self.client.post(
            path,
            data={
                "username": "segundo-administrador",
                "password1": "SenhaSegura123!",
                "password2": "SenhaSegura123!",
            },
        )

        self.assertEqual(get_response.status_code, 404)
        self.assertEqual(post_response.status_code, 404)
        self.assertFalse(
            User.objects.filter(username="segundo-administrador").exists()
        )

    def test_delete_view_get_displays_confirmation_page(self):
        response = self.client.get(
            reverse(
                "accounts:accounts_delete",
                kwargs={"username": self.user.username},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_confirm_delete.html",
        )
        self.assertEqual(response.context["object"], self.user)

    def test_delete_view_post_deletes_account_and_redirects(self):
        response = self.client.post(
            reverse(
                "accounts:accounts_delete",
                kwargs={"username": self.user.username},
            )
        )

        self.assertRedirects(
            response,
            reverse("accounts:accounts_list"),
            fetch_redirect_response=False,
        )
        self.assertFalse(
            User.objects.filter(pk=self.user.pk).exists()
        )

    def test_object_views_return_not_found_for_unknown_account(self):
        response = self.client.get(
            reverse(
                "accounts:accounts_delete",
                kwargs={"username": "usuario-inexistente"},
            )
        )

        self.assertEqual(response.status_code, 404)


@override_settings(TEMPLATES=TEMPLATES)
class InitialAdminSetupConcurrencyTest(TransactionTestCase):

    @classmethod
    def setUpTestData(cls):
        Group.objects.create(name="admin")

    def test_only_one_concurrent_request_can_create_initial_admin(self):
        path = reverse("accounts:accounts_initial_admin_create")
        barrier = Barrier(2)
        original_post = InitialAdminCreateView.post

        def synchronized_post(view, request, *args, **kwargs):
            barrier.wait(timeout=10)
            return original_post(view, request, *args, **kwargs)

        def create_initial_admin(username):
            close_old_connections()
            try:
                return Client().post(
                    path,
                    data={
                        "username": username,
                        "password1": "SenhaSegura123!",
                        "password2": "SenhaSegura123!",
                    },
                ).status_code
            finally:
                close_old_connections()

        with patch.object(
            InitialAdminCreateView,
            "post",
            synchronized_post,
        ):
            with ThreadPoolExecutor(max_workers=2) as executor:
                statuses = list(
                    executor.map(
                        create_initial_admin,
                        ("admin-concorrente-1", "admin-concorrente-2"),
                    )
                )

        self.assertCountEqual(statuses, [302, 404])
        self.assertEqual(User.objects.count(), 1)
