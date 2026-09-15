from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from apps.resources.models import Resource
from apps.tickets.models import Ticket
from apps.tickets.views import (
    TicketCreateView,
    TicketDeleteView,
    TicketDetailView,
    TicketListView,
    TickerUpdateView,
)

User = get_user_model()


class TicketUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="usuario-teste",
            password="senha-segura-123",
        )
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )
        cls.ticket = Ticket.objects.create(
            titulo="Projetor",
            descricao="O projetor não liga.",
            usuario=cls.user,
            resource=cls.resource,
        )

    def test_ticket_urls_reverse_to_expected_paths(self):
        expected_urls = {
            "ticket_list": ("/chamados/", {}),
            "ticket_create": ("/chamados/create/", {}),
            "ticket_detail": (
                "/chamados/chamado/Projetor",
                {"titulo": self.ticket.titulo},
            ),
            "ticket_update": (
                "/chamados/update/Projetor",
                {"titulo": self.ticket.titulo},
            ),
            "ticket_delete": (
                "/chamados/delete/Projetor/",
                {"titulo": self.ticket.titulo},
            ),
        }

        for url_name, (expected_path, kwargs) in expected_urls.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    reverse(f"tickets:{url_name}", kwargs=kwargs),
                    expected_path,
                )

    def test_ticket_urls_resolve_to_expected_views(self):
        expected_views = {
            "ticket_list": TicketListView,
            "ticket_create": TicketCreateView,
            "ticket_detail": TicketDetailView,
            "ticket_update": TickerUpdateView,
            "ticket_delete": TicketDeleteView,
        }

        for url_name, expected_view in expected_views.items():
            kwargs = (
                {}
                if url_name in {"ticket_list", "ticket_create"}
                else {"titulo": self.ticket.titulo}
            )

            with self.subTest(url_name=url_name):
                resolved_url = resolve(
                    reverse(f"tickets:{url_name}", kwargs=kwargs)
                )

                self.assertIs(resolved_url.func.view_class, expected_view)

    def test_ticket_urls_return_successful_responses(self):
        url_kwargs = {
            "ticket_list": {},
            "ticket_create": {},
            "ticket_detail": {"titulo": self.ticket.titulo},
            "ticket_update": {"titulo": self.ticket.titulo},
            "ticket_delete": {"titulo": self.ticket.titulo},
        }

        for url_name, kwargs in url_kwargs.items():
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(f"tickets:{url_name}", kwargs=kwargs)
                )

                self.assertEqual(response.status_code, 200)