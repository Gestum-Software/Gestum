from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase, override_settings
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


@override_settings(TEMPLATES=TEMPLATES)
class AccountsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.group = Group.objects.create(name="Administradores")
        cls.admin_group, _ = Group.objects.get_or_create(name="admin")
        cls.user = User.objects.create_user(
            username="usuario-teste",
            password="SenhaSegura123!",
        )
        cls.user.groups.add(cls.group)

    def test_list_view_returns_accounts(self):
        response = self.client.get(reverse("accounts:accounts_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_list.html",
        )
        self.assertIn(self.user, response.context["object_list"])

    def test_login_view_get_displays_form(self):
        response = self.client.get(reverse("accounts:accounts_login"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "accounts/accounts_login.html",
        )
        self.assertIsInstance(response.context["view"], AccountsLoginView)
        self.assertEqual(response.context["form"].initial, {})

    def test_login_view_post_authenticates_user_and_redirects(self):
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
            "groups": [str(self.group.pk)],
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
        self.assertEqual(User.objects.count(), 1)

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
