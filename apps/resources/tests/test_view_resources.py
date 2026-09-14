from django.test import TestCase
from django.urls import reverse

from apps.resources.models import Resource


class ResourcesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )

    def test_list_view_returns_resources(self):
        response = self.client.get(reverse("resource:resource_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resource_list.html")
        self.assertIn(self.resource, response.context["object_list"])

    def test_create_view_get_displays_form(self):
        response = self.client.get(reverse("resource:resource_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resource_form.html")

        form = response.context["form"]

        self.assertIsInstance(form.instance, Resource)
        self.assertIsNone(form.instance.pk)

    def test_create_view_post_creates_resource_and_redirects(self):
        resource_data = {
            "nome": "Notebook",
            "observacoes": "Notebook disponível para empréstimo.",
        }

        response = self.client.post(
            reverse("resource:resource_create"),
            data=resource_data,
        )

        created_resource = Resource.objects.get(nome=resource_data["nome"])

        self.assertRedirects(response, reverse("resource:resource_list"))
        self.assertEqual(created_resource.observacoes, resource_data["observacoes"])
        self.assertEqual(
            created_resource.status,
            Resource.StatusChoices.DISPONIVEL,
        )

    def test_create_view_post_with_invalid_data_does_not_create_resource(self):
        response = self.client.post(
            reverse("resource:resource_create"),
            data={"nome": "", "observacoes": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resource_form.html")
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Resource.objects.count(), 1)

    def test_detail_view_returns_requested_resource(self):
        response = self.client.get(
            reverse(
                "resource:resource_detail",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resource_detail.html")
        self.assertEqual(response.context["object"], self.resource)

    def test_update_view_get_displays_resource_form(self):
        response = self.client.get(
            reverse(
                "resource:resource_update",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "resources/resource_form.html")
        self.assertEqual(response.context["form"].instance, self.resource)

    def test_update_view_post_updates_resource_and_redirects(self):
        response = self.client.post(
            reverse(
                "resource:resource_update",
                kwargs={"nome": self.resource.nome},
            ),
            data={
                "nome": "Projetor atualizado",
                "observacoes": "Projetor revisado.",
            },
        )

        self.resource.refresh_from_db()

        self.assertRedirects(response, reverse("resource:resource_list"))
        self.assertEqual(self.resource.nome, "Projetor atualizado")
        self.assertEqual(self.resource.observacoes, "Projetor revisado.")

    def test_delete_view_get_displays_confirmation_page(self):
        response = self.client.get(
            reverse(
                "resource:resource_delete",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "resources/resource_confirm_delete.html",
        )
        self.assertEqual(response.context["object"], self.resource)

    def test_delete_view_post_deletes_resource_and_redirects(self):
        response = self.client.post(
            reverse(
                "resource:resource_delete",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertRedirects(response, reverse("resource:resource_list"))
        self.assertFalse(
            Resource.objects.filter(pk=self.resource.pk).exists()
        )

    def test_views_return_not_found_for_unknown_resource(self):
        resource_urls = (
            "resource:resource_detail",
            "resource:resource_update",
            "resource:resource_delete",
        )

        for url_name in resource_urls:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(
                        url_name,
                        kwargs={"nome": "Recurso inexistente"},
                    )
                )

                self.assertEqual(response.status_code, 404)
