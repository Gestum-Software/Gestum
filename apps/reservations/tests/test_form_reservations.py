from django import forms
from django.test import TestCase

from apps.reservations.forms import ReservationForm
from apps.resources.models import Resource


class ReservationFormTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )

    def form_data(self, **overrides):
        data = {
            "titulo": "Apresentação trimestral",
            "observacoes": "Reserva para a apresentação da equipe.",
            "inicio": "2026-09-16 10:00",
            "fim": "2026-09-16 12:00",
            "resource": self.resource.pk,
        }
        data.update(overrides)
        return data

    def test_form_has_expected_fields(self):
        form = ReservationForm()

        self.assertEqual(
            list(form.fields),
            ["titulo", "observacoes", "inicio", "fim", "resource"],
        )
        self.assertNotIn("usuario", form.fields)

    def test_form_uses_expected_widgets(self):
        form = ReservationForm()

        self.assertIsInstance(form.fields["titulo"].widget, forms.TextInput)
        self.assertEqual(
            form.fields["titulo"].widget.attrs["class"],
            "campo-titulo",
        )
        self.assertEqual(
            form.fields["titulo"].widget.attrs["placeholder"],
            "Titulo da reserva",
        )
        self.assertEqual(
            form.fields["observacoes"].widget.attrs["class"],
            "campo-observacoes campo",
        )
        self.assertEqual(
            form.fields["observacoes"].widget.attrs["maxlength"],
            "1500",
        )
        self.assertIsInstance(
            form.fields["observacoes"].widget,
            forms.Textarea,
        )
        self.assertIsInstance(form.fields["inicio"].widget, forms.DateInput)
        self.assertIsInstance(form.fields["fim"].widget, forms.DateInput)
        self.assertEqual(form.fields["inicio"].widget.input_type, "date")
        self.assertEqual(form.fields["fim"].widget.input_type, "date")
        self.assertIsInstance(form.fields["resource"].widget, forms.Select)
        self.assertEqual(
            form.fields["resource"].widget.attrs["class"],
            "campo-recursos",
        )

    def test_form_accepts_valid_data(self):
        form = ReservationForm(data=self.form_data())

        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["resource"], self.resource)
        self.assertEqual(form.cleaned_data["titulo"], "Apresentação trimestral")

    def test_form_rejects_missing_required_fields(self):
        data = self.form_data(
            titulo="",
            observacoes="",
            inicio="",
            fim="",
            resource="",
        )

        form = ReservationForm(data=data)

        self.assertFalse(form.is_valid())
        for field_name in ("titulo", "observacoes", "inicio", "fim", "resource"):
            with self.subTest(field=field_name):
                self.assertIn(field_name, form.errors)

    def test_form_rejects_title_longer_than_allowed(self):
        form = ReservationForm(data=self.form_data(titulo="t" * 51))

        self.assertFalse(form.is_valid())
        self.assertIn("titulo", form.errors)

    def test_form_rejects_observations_longer_than_allowed(self):
        form = ReservationForm(
            data=self.form_data(observacoes="o" * 1501),
        )

        self.assertFalse(form.is_valid())
        self.assertIn("observacoes", form.errors)

    def test_form_rejects_end_before_or_equal_to_start(self):
        for end in ("2026-09-16 10:00", "2026-09-16 09:59"):
            with self.subTest(end=end):
                form = ReservationForm(data=self.form_data(fim=end))

                self.assertFalse(form.is_valid())
                self.assertIn("__all__", form.errors)
                self.assertIn(
                    "A data de término deve ser posterior à data de início.",
                    form.non_field_errors(),
                )
