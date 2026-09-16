from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.test import TestCase
from django.utils import timezone

from apps.reservations.models import Reservation
from apps.resources.models import Resource


class ReservationModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reservation-user",
            password="test-password",
        )
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )
        cls.inicio = timezone.now().replace(microsecond=0)
        cls.fim = cls.inicio + timedelta(hours=2)

    def create_reservation(self, **kwargs):
        reservation_data = {
            "titulo": "Apresentação trimestral",
            "observacoes": "Reserva para a apresentação da equipe.",
            "inicio": self.inicio,
            "fim": self.fim,
            "usuario": self.user,
            "resource": self.resource,
        }
        reservation_data.update(kwargs)
        return Reservation.objects.create(**reservation_data)

    def test_create_reservation_with_required_fields(self):
        reservation = self.create_reservation()

        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(reservation.titulo, "Apresentação trimestral")
        self.assertEqual(
            reservation.observacoes,
            "Reserva para a apresentação da equipe.",
        )
        self.assertEqual(reservation.inicio, self.inicio)
        self.assertEqual(reservation.fim, self.fim)
        self.assertEqual(reservation.usuario, self.user)
        self.assertEqual(reservation.resource, self.resource)

    def test_model_field_configuration(self):
        titulo = Reservation._meta.get_field("titulo")
        observacoes = Reservation._meta.get_field("observacoes")
        inicio = Reservation._meta.get_field("inicio")
        fim = Reservation._meta.get_field("fim")
        usuario = Reservation._meta.get_field("usuario")
        resource = Reservation._meta.get_field("resource")

        self.assertEqual(titulo.max_length, 50)
        self.assertEqual(observacoes.max_length, 1500)
        self.assertFalse(observacoes.blank)
        self.assertFalse(observacoes.null)
        self.assertIsInstance(inicio, models.DateTimeField)
        self.assertIsInstance(fim, models.DateTimeField)
        self.assertEqual(usuario.remote_field.related_name, "reservations")
        self.assertEqual(usuario.remote_field.on_delete, models.CASCADE)
        self.assertEqual(resource.remote_field.on_delete, models.CASCADE)

    def test_full_clean_accepts_reservation_with_end_after_start(self):
        reservation = Reservation(**{
            "titulo": "Apresentação trimestral",
            "observacoes": "Reserva para a apresentação da equipe.",
            "inicio": self.inicio,
            "fim": self.fim,
            "usuario": self.user,
            "resource": self.resource,
        })

        reservation.full_clean()

    def test_full_clean_rejects_reservation_when_end_is_not_after_start(self):
        invalid_end_times = [self.inicio, self.inicio - timedelta(minutes=1)]

        for invalid_end in invalid_end_times:
            with self.subTest(invalid_end=invalid_end):
                reservation = Reservation(
                    titulo="Apresentação trimestral",
                    observacoes="Reserva para a apresentação da equipe.",
                    inicio=self.inicio,
                    fim=invalid_end,
                    usuario=self.user,
                    resource=self.resource,
                )

                with self.assertRaisesRegex(
                    ValidationError,
                    "A data de término deve ser posterior à data de início.",
                ):
                    reservation.full_clean()

    def test_deleting_user_deletes_related_reservations(self):
        self.create_reservation()

        self.user.delete()

        self.assertEqual(Reservation.objects.count(), 0)

    def test_deleting_resource_deletes_related_reservations(self):
        self.create_reservation()

        self.resource.delete()

        self.assertEqual(Reservation.objects.count(), 0)
