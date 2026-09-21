from django.contrib.auth import get_user_model
from django.test import TestCase


User = get_user_model()


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="usuario-teste",
            email="usuario@example.com",
            password="senha-segura-123",
        )

    def test_create_user_with_required_fields(self):
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.user.username, "usuario-teste")
        self.assertEqual(self.user.email, "usuario@example.com")
        self.assertTrue(self.user.is_active)

    def test_create_user_hashes_password(self):
        self.assertNotEqual(self.user.password, "senha-segura-123")
        self.assertTrue(self.user.check_password("senha-segura-123"))

    def test_string_representation(self):
        self.assertEqual(str(self.user), "usuario-teste")

    def test_user_defaults(self):
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_username_field_configuration(self):
        username = User._meta.get_field("username")

        self.assertEqual(username.max_length, 150)
        self.assertTrue(username.unique)
        self.assertFalse(username.blank)
        self.assertFalse(username.null)