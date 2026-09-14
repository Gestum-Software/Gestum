from django.test import TestCase
from django.urls import resolve, reverse

from apps.resources.models import Resource
from apps.resources.views import (
    ResourceDeleteView,
    ResourceDetailView,
    ResourcesCreateView,
    ResourcesListView,
    ResourceUpdateView,
)


class ResourcesUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )

    def test_resource_urls_reverse_to_expected_paths(self):
        expected_urls = {
            "resource_list": ("/recursos/", {}),
            "resource_create": ("/recursos/create/", {}),
            "resource_detail": (
                "/recursos/recurso/Projetor/",
                {"nome": self.resource.nome},
            ),
            "resource_update": (
                "/recursos/update/Projetor",
                {"nome": self.resource.nome},
            ),
            "resource_delete": (
                "/recursos/delete/Projetor",
                {"nome": self.resource.nome},
            ),
        }

        for url_name, (expected_path, kwargs) in expected_urls.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    reverse(f"resource:{url_name}", kwargs=kwargs),
                    expected_path,
                )

    def test_resource_urls_resolve_to_expected_views(self):
        expected_views = {
            "resource_list": ResourcesListView,
            "resource_create": ResourcesCreateView,
            "resource_detail": ResourceDetailView,
            "resource_update": ResourceUpdateView,
            "resource_delete": ResourceDeleteView,
        }

        for url_name, expected_view in expected_views.items():
            kwargs = (
                {}
                if url_name in {"resource_list", "resource_create"}
                else {"nome": self.resource.nome}
            )

            with self.subTest(url_name=url_name):
                resolved_url = resolve(
                    reverse(f"resource:{url_name}", kwargs=kwargs)
                )

                self.assertIs(resolved_url.func.view_class, expected_view)

    def test_resource_list_url_returns_success(self):
        response = self.client.get(reverse("resource:resource_list"))

        self.assertEqual(response.status_code, 200)

    def test_resource_create_url_returns_success(self):
        response = self.client.get(reverse("resource:resource_create"))

        self.assertEqual(response.status_code, 200)

    def test_resource_detail_url_returns_success(self):
        response = self.client.get(
            reverse(
                "resource:resource_detail",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_resource_update_url_returns_success(self):
        response = self.client.get(
            reverse(
                "resource:resource_update",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_resource_delete_url_returns_success(self):
        response = self.client.get(
            reverse(
                "resource:resource_delete",
                kwargs={"nome": self.resource.nome},
            )
        )

        self.assertEqual(response.status_code, 200)
