from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from apps.accounts.forms import (
    CustomUserCreationForm,
    CustomUserWithGroupsCreationForm,
)


User = get_user_model()


class CustomUserCreationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.existing_user = User.objects.create_user(
            username="usuario-existente",
            password="SenhaSegura123!",
        )

    def valid_form_data(self, **overrides):
        data = {
            "username": "novo-usuario",
            "password": "SenhaSegura123!",
            "password1": "SenhaSegura123!",
            "password2": "SenhaSegura123!",
        }
        data.update(overrides)
        return data

    def test_form_exposes_expected_fields(self):
        form = CustomUserCreationForm()

        self.assertEqual(
            list(form.fields),
            ["username", "password", "password1", "password2"],
        )

    def test_form_uses_expected_widgets_and_attributes(self):
        form = CustomUserCreationForm()

        self.assertIsInstance(form.fields["username"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["username"].widget.attrs,
            {
                "maxlength": "150",
                "autocapitalize": "none",
                "autocomplete": "username",
                "autofocus": True,
                "class": "campo-nome",
                "placeholder": "Digite o nome",
            },
        )
        self.assertEqual(
            form.fields["password"].widget.attrs,
            {
                "maxlength": "128",
                "class": "campo-senha",
                "placeholder": "Digite a senha",
            },
        )

    def test_form_accepts_valid_data_and_hashes_password_on_save(self):
        form = CustomUserCreationForm(data=self.valid_form_data())

        self.assertTrue(form.is_valid(), form.errors.as_text())
        user = form.save()

        self.assertEqual(user.username, "novo-usuario")
        self.assertNotEqual(user.password, "SenhaSegura123!")
        self.assertTrue(user.check_password("SenhaSegura123!"))

    def test_form_rejects_missing_required_fields(self):
        form = CustomUserCreationForm(
            data=self.valid_form_data(
                username="",
                password="",
                password1="",
                password2="",
            ),
        )

        self.assertFalse(form.is_valid())
        for field_name in ("username", "password", "password1", "password2"):
            with self.subTest(field=field_name):
                self.assertIn(field_name, form.errors)
                self.assertEqual(
                    form.errors.as_data()[field_name][0].code,
                    "required",
                )

    def test_form_rejects_mismatched_password_confirmation(self):
        form = CustomUserCreationForm(
            data=self.valid_form_data(password2="OutraSenha123!"),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["password2"][0].code,
            "password_mismatch",
        )

    def test_form_rejects_duplicate_username_case_insensitively(self):
        form = CustomUserCreationForm(
            data=self.valid_form_data(username="USUARIO-EXISTENTE"),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)


class CustomUserWithGroupsCreationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.administrator_group = Group.objects.create(name="Administradores")
        cls.support_group = Group.objects.create(name="Suporte")

    def valid_form_data(self, **overrides):
        data = {
            "username": "usuario-com-grupos",
            "password": "SenhaSegura123!",
            "password1": "SenhaSegura123!",
            "password2": "SenhaSegura123!",
            "groups": [
                self.administrator_group.pk,
                self.support_group.pk,
            ],
        }
        data.update(overrides)
        return data

    def test_form_declares_groups_as_multiple_choice_checkbox_field(self):
        form = CustomUserWithGroupsCreationForm()
        field = form.fields["groups"]

        self.assertIsInstance(field, forms.ModelMultipleChoiceField)
        self.assertIsInstance(field.widget, forms.CheckboxSelectMultiple)
        self.assertEqual(field.label, "Selecione os perfis")
        self.assertEqual(field.widget.attrs, {"class": "campo-grupo"})

    def test_form_saves_user_with_selected_groups(self):
        form = CustomUserWithGroupsCreationForm(data=self.valid_form_data())

        self.assertTrue(form.is_valid(), form.errors.as_text())
        user = form.save()

        self.assertEqual(
            set(user.groups.values_list("pk", flat=True)),
            {self.administrator_group.pk, self.support_group.pk},
        )

    def test_form_requires_at_least_one_group(self):
        form = CustomUserWithGroupsCreationForm(
            data=self.valid_form_data(groups=[]),
        )

        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors.as_data()["groups"][0].code,
            "required",
        )

    def test_form_save_without_commit_preserves_group_m2m_callback(self):
        form = CustomUserWithGroupsCreationForm(data=self.valid_form_data())

        self.assertTrue(form.is_valid(), form.errors.as_text())
        user = form.save(commit=False)

        self.assertFalse(User.objects.filter(username=user.username).exists())
        user.save()
        form.save_m2m()

        self.assertEqual(
            set(user.groups.values_list("pk", flat=True)),
            {self.administrator_group.pk, self.support_group.pk},
        )