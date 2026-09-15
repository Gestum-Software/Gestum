from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.resources.models import Resource
from apps.tickets.models import Ticket

User = get_user_model()


class TicketViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="usuario-teste",
            password="senha-segura",
        )
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )
        cls.ticket = Ticket.objects.create(
            titulo="Projetor não liga",
            descricao="O projetor não liga ao pressionar o botão.",
            usuario=cls.user,
            resource=cls.resource,
        )

    def test_list_view_returns_tickets(self):
        response = self.client.get(reverse("tickets:ticket_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticket_list.html")
        self.assertIn(self.ticket, response.context["object_list"])

    def test_create_view_get_displays_form(self):
        response = self.client.get(reverse("tickets:ticket_create"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticket_form.html")
        self.assertIsInstance(response.context["form"].instance, Ticket)
        self.assertIsNone(response.context["form"].instance.pk)

    def test_create_view_post_with_invalid_data_does_not_create_ticket(self):
        response = self.client.post(
            reverse("tickets:ticket_create"),
            data={"titulo": "", "descricao": ""},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticket_form.html")
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Ticket.objects.count(), 1)

    def test_detail_view_returns_requested_ticket(self):
        response = self.client.get(
            reverse(
                "tickets:ticket_detail",
                kwargs={"titulo": self.ticket.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticket_detail.html")
        self.assertEqual(response.context["object"], self.ticket)

    def test_update_view_get_displays_ticket_form(self):
        response = self.client.get(
            reverse(
                "tickets:ticket_update",
                kwargs={"titulo": self.ticket.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "tickets/ticket_form.html")
        self.assertEqual(response.context["form"].instance, self.ticket)

    def test_update_view_post_updates_ticket_and_redirects(self):
        response = self.client.post(
            reverse(
                "tickets:ticket_update",
                kwargs={"titulo": self.ticket.titulo},
            ),
            data={
                "titulo": "Projetor revisado",
                "descricao": "O projetor foi revisado pela equipe.",
            },
        )

        self.ticket.refresh_from_db()

        self.assertRedirects(response, reverse("tickets:ticket_list"))
        self.assertEqual(self.ticket.titulo, "Projetor revisado")
        self.assertEqual(
            self.ticket.descricao,
            "O projetor foi revisado pela equipe.",
        )
        self.assertEqual(self.ticket.usuario, self.user)
        self.assertEqual(self.ticket.resource, self.resource)

    def test_delete_view_get_displays_confirmation_page(self):
        response = self.client.get(
            reverse(
                "tickets:ticket_delete",
                kwargs={"titulo": self.ticket.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "tickets/ticket_confirm_delete.html",
        )
        self.assertEqual(response.context["object"], self.ticket)

    def test_delete_view_post_deletes_ticket_and_redirects(self):
        response = self.client.post(
            reverse(
                "tickets:ticket_delete",
                kwargs={"titulo": self.ticket.titulo},
            )
        )

        self.assertRedirects(response, reverse("tickets:ticket_list"))
        self.assertFalse(
            Ticket.objects.filter(pk=self.ticket.pk).exists()
        )

    def test_object_views_return_not_found_for_unknown_ticket(self):
        ticket_urls = (
            "tickets:ticket_detail",
            "tickets:ticket_update",
            "tickets:ticket_delete",
        )

        for url_name in ticket_urls:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(
                        url_name,
                        kwargs={"titulo": "Chamado inexistente"},
                    )
                )

                self.assertEqual(response.status_code, 404)
