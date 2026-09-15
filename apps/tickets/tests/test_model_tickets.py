from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.resources.models import Resource
from apps.tickets.models import Ticket

User = get_user_model()


class TicketModelTest(TestCase):

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

    def test_create_ticket_with_required_fields(self):
        ticket = Ticket.objects.create(
            titulo="Projetor não liga",
            descricao="O projetor não liga ao pressionar o botão.",
            usuario=self.user,
            resource=self.resource,
        )

        self.assertEqual(Ticket.objects.count(), 1)
        self.assertEqual(ticket.titulo, "Projetor não liga")
        self.assertEqual(
            ticket.descricao,
            "O projetor não liga ao pressionar o botão.",
        )
        self.assertEqual(ticket.usuario, self.user)
        self.assertEqual(ticket.resource, self.resource)

    def test_status_defaults_to_open(self):
        ticket = Ticket.objects.create(
            titulo="Projetor não liga",
            descricao="O projetor não liga ao pressionar o botão.",
            usuario=self.user,
            resource=self.resource,
        )

        self.assertEqual(ticket.status, Ticket.StatusChoices.ABERTO)

    def test_status_can_be_set_to_finished(self):
        ticket = Ticket.objects.create(
            titulo="Projetor não liga",
            descricao="O projetor foi reparado.",
            status=Ticket.StatusChoices.FINALIZADO,
            usuario=self.user,
            resource=self.resource,
        )

        self.assertEqual(ticket.status, Ticket.StatusChoices.FINALIZADO)

    def test_status_choices_are_defined(self):
        self.assertEqual(
            Ticket.StatusChoices.choices,
            [
                ("aberto", "Aberto"),
                ("finalizado", "Finalizado"),
            ],
        )

    def test_model_field_configuration(self):
        titulo = Ticket._meta.get_field("titulo")
        descricao = Ticket._meta.get_field("descricao")
        status = Ticket._meta.get_field("status")
        usuario = Ticket._meta.get_field("usuario")
        resource = Ticket._meta.get_field("resource")

        self.assertEqual(titulo.max_length, 50)
        self.assertEqual(descricao.max_length, 1500)
        self.assertFalse(descricao.blank)
        self.assertFalse(descricao.null)
        self.assertEqual(status.max_length, 20)
        self.assertEqual(status.default, Ticket.StatusChoices.ABERTO)
        self.assertEqual(usuario.remote_field.model, User)
        self.assertEqual(usuario.remote_field.related_name, "meus_modelos")
        self.assertEqual(resource.remote_field.model, Resource)
