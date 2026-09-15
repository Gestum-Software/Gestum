from django import forms
from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.resources.models import Resource
from apps.tickets.forms import TicketForm
from apps.tickets.models import Ticket

User = get_user_model()


class TicketFormTest(TestCase):

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
            titulo="Projetor não liga",
            descricao="O projetor não liga ao pressionar o botão.",
            usuario=cls.user,
            resource=cls.resource,
        )

    def test_form_exposes_only_editable_ticket_fields(self):
        form = TicketForm()

        self.assertEqual(list(form.fields), ["titulo", "descricao"])
        self.assertNotIn("status", form.fields)
        self.assertNotIn("usuario", form.fields)
        self.assertNotIn("resource", form.fields)

    def test_form_uses_expected_widgets_and_attributes(self):
        form = TicketForm()

        self.assertIsInstance(form.fields["titulo"].widget, forms.TextInput)
        self.assertIsInstance(
            form.fields["descricao"].widget,
            forms.Textarea,
        )
        self.assertEqual(
            form.fields["titulo"].widget.attrs,
            {
                "class": "campo-titulo",
                "placeholder": "Titulo do chamado",
                "maxlength": "50",
            },
        )
        self.assertEqual(
            form.fields["descricao"].widget.attrs,
            {
                "cols": "40",
                "class": "campo-descricao",
                "maxlength": "1500",
                "placeholder": "Descrição do chamado",
                "rows": "10",
            },
        )

    def test_form_is_valid_with_required_data(self):
        form = TicketForm(
            data={
                "titulo": "Computador não liga",
                "descricao": "O computador não liga ao ser iniciado.",
            }
        )

        self.assertTrue(form.is_valid(), form.errors.as_text())
        self.assertEqual(form.cleaned_data["titulo"], "Computador não liga")
        self.assertEqual(
            form.cleaned_data["descricao"],
            "O computador não liga ao ser iniciado.",
        )

    def test_form_requires_title_and_description(self):
        form = TicketForm(data={"titulo": "", "descricao": ""})

        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)
        self.assertIn("descricao", form.errors)
        errors = form.errors.as_data()
        self.assertEqual(errors["titulo"][0].code, "required")
        self.assertEqual(errors["descricao"][0].code, "required")

    def test_form_rejects_values_exceeding_model_field_limits(self):
        form = TicketForm(
            data={
                "titulo": "T" * 51,
                "descricao": "D" * 1501,
            }
        )

        self.assertFalse(form.is_valid())
        errors = form.errors.as_data()
        self.assertEqual(errors["titulo"][0].code, "max_length")
        self.assertEqual(errors["descricao"][0].code, "max_length")

    def test_form_can_edit_existing_ticket_without_changing_excluded_fields(self):
        form = TicketForm(
            data={
                "titulo": "Projetor revisado",
                "descricao": "O projetor foi revisado pela equipe.",
            },
            instance=self.ticket,
        )

        self.assertTrue(form.is_valid(), form.errors.as_text())
        updated_ticket = form.save()

        self.assertEqual(updated_ticket.pk, self.ticket.pk)
        self.assertEqual(updated_ticket.titulo, "Projetor revisado")
        self.assertEqual(
            updated_ticket.descricao,
            "O projetor foi revisado pela equipe.",
        )
        self.assertEqual(updated_ticket.status, Ticket.StatusChoices.ABERTO)
        self.assertEqual(updated_ticket.usuario, self.user)
        self.assertEqual(updated_ticket.resource, self.resource)