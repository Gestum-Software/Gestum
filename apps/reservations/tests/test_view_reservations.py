from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from apps.reservations.models import Reservation
from apps.resources.models import Resource


class ReservationViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reservation-view-user",
            password="test-password",
        )
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )
        cls.inicio = timezone.now().replace(microsecond=0)
        cls.fim = cls.inicio + timedelta(hours=2)
        cls.reservation = Reservation.objects.create(
            titulo="Apresentação trimestral",
            observacoes="Reserva para a apresentação da equipe.",
            inicio=cls.inicio,
            fim=cls.fim,
            usuario=cls.user,
            resource=cls.resource,
        )

    def setUp(self):
        self.client.force_login(self.user)

    def reservation_data(self, **overrides):
        data = {
            "titulo": "Reunião de planejamento",
            "observacoes": "Reserva para a reunião da equipe.",
            "inicio": "2026-09-16 10:00",
            "fim": "2026-09-16 12:00",
            "resource": self.resource.pk,
        }
        data.update(overrides)
        return data

    def test_list_view_returns_reservations(self):
        response = self.client.get(
            reverse("reservations:reservation_list"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_list.html",
        )
        self.assertIn(self.reservation, response.context["object_list"])

    def test_create_view_get_displays_form(self):
        response = self.client.get(
            reverse("reservations:reservation_create"),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_form.html",
        )
        self.assertIsInstance(response.context["form"].instance, Reservation)
        self.assertIsNone(response.context["form"].instance.pk)

    def test_create_view_post_creates_reservation_and_redirects(self):
        response = self.client.post(
            reverse("reservations:reservation_create"),
            data=self.reservation_data(),
        )

        created_reservation = Reservation.objects.get(
            titulo="Reunião de planejamento",
        )

        self.assertRedirects(
            response,
            reverse("reservations:reservation_list"),
        )
        self.assertEqual(created_reservation.usuario, self.user)
        self.assertEqual(created_reservation.resource, self.resource)
        self.assertEqual(
            created_reservation.observacoes,
            "Reserva para a reunião da equipe.",
        )

    def test_create_view_post_with_invalid_data_does_not_create_reservation(
        self,
    ):
        response = self.client.post(
            reverse("reservations:reservation_create"),
            data=self.reservation_data(
                titulo="",
                inicio="2026-09-16 12:00",
                fim="2026-09-16 10:00",
            ),
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_form.html",
        )
        self.assertTrue(response.context["form"].errors)
        self.assertEqual(Reservation.objects.count(), 1)

    def test_detail_view_returns_requested_reservation(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_detail",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_detail.html",
        )
        self.assertEqual(response.context["object"], self.reservation)

    def test_update_view_get_displays_reservation_form(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_update",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_form.html",
        )
        self.assertEqual(
            response.context["form"].instance,
            self.reservation,
        )

    def test_update_view_post_updates_reservation_and_redirects(self):
        response = self.client.post(
            reverse(
                "reservations:reservation_update",
                kwargs={"titulo": self.reservation.titulo},
            ),
            data=self.reservation_data(
                titulo="Apresentação trimestral atualizada",
                observacoes="Reserva revisada.",
            ),
        )

        self.reservation.refresh_from_db()

        self.assertRedirects(
            response,
            reverse("reservations:reservation_list"),
        )
        self.assertEqual(
            self.reservation.titulo,
            "Apresentação trimestral atualizada",
        )
        self.assertEqual(self.reservation.observacoes, "Reserva revisada.")
        self.assertEqual(self.reservation.usuario, self.user)

    def test_delete_view_get_displays_confirmation_page(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_delete",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response,
            "reservations/reservation_confirm_delete.html",
        )
        self.assertEqual(response.context["object"], self.reservation)

    def test_delete_view_post_deletes_reservation_and_redirects(self):
        response = self.client.post(
            reverse(
                "reservations:reservation_delete",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertRedirects(
            response,
            reverse("reservations:reservation_list"),
        )
        self.assertFalse(
            Reservation.objects.filter(pk=self.reservation.pk).exists(),
        )

    def test_views_return_not_found_for_unknown_reservation(self):
        reservation_urls = (
            "reservations:reservation_detail",
            "reservations:reservation_update",
            "reservations:reservation_delete",
        )

        for url_name in reservation_urls:
            with self.subTest(url_name=url_name):
                response = self.client.get(
                    reverse(
                        url_name,
                        kwargs={"titulo": "Reserva inexistente"},
                    )
                )

                self.assertEqual(response.status_code, 404)