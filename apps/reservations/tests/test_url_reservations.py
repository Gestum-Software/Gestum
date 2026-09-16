from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse
from django.utils import timezone

from apps.reservations.models import Reservation
from apps.reservations.views import (
    ReservationCreateView,
    ReservationDeleteView,
    ReservationDetailView,
    ReservationListView,
    ReservationUpdateView,
)
from apps.resources.models import Resource


class ReservationsUrlTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="reservation-url-user",
            password="test-password",
        )
        cls.resource = Resource.objects.create(
            nome="Projetor",
            observacoes="Projetor disponível para empréstimo.",
        )
        cls.inicio = timezone.now()
        cls.reservation = Reservation.objects.create(
            titulo="Apresentacao trimestral",
            observacoes="Reserva para a apresentação da equipe.",
            inicio=cls.inicio,
            fim=cls.inicio + timedelta(hours=2),
            usuario=cls.user,
            resource=cls.resource,
        )

    def test_reservation_urls_reverse_to_expected_paths(self):
        expected_urls = {
            "reservation_list": ("/reservas/", {}),
            "reservation_create": ("/reservas/create/", {}),
            "reservation_detail": (
                "/reservas/reserva/Apresentacao%20trimestral",
                {"titulo": self.reservation.titulo},
            ),
            "reservation_update": (
                "/reservas/update/Apresentacao%20trimestral",
                {"titulo": self.reservation.titulo},
            ),
            "reservation_delete": (
                "/reservas/delete/Apresentacao%20trimestral",
                {"titulo": self.reservation.titulo},
            ),
        }

        for url_name, (expected_path, kwargs) in expected_urls.items():
            with self.subTest(url_name=url_name):
                self.assertEqual(
                    reverse(f"reservations:{url_name}", kwargs=kwargs),
                    expected_path,
                )

    def test_reservation_urls_resolve_to_expected_views(self):
        expected_views = {
            "reservation_list": ReservationListView,
            "reservation_create": ReservationCreateView,
            "reservation_detail": ReservationDetailView,
            "reservation_update": ReservationUpdateView,
            "reservation_delete": ReservationDeleteView,
        }

        for url_name, expected_view in expected_views.items():
            kwargs = (
                {}
                if url_name in {"reservation_list", "reservation_create"}
                else {"titulo": self.reservation.titulo}
            )

            with self.subTest(url_name=url_name):
                resolved_url = resolve(
                    reverse(f"reservations:{url_name}", kwargs=kwargs)
                )

                self.assertIs(resolved_url.func.view_class, expected_view)

    def test_reservation_list_url_returns_success(self):
        response = self.client.get(
            reverse("reservations:reservation_list"),
        )

        self.assertEqual(response.status_code, 200)

    def test_reservation_create_url_returns_success(self):
        response = self.client.get(
            reverse("reservations:reservation_create"),
        )

        self.assertEqual(response.status_code, 200)

    def test_reservation_detail_url_returns_success(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_detail",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_reservation_update_url_returns_success(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_update",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)

    def test_reservation_delete_url_returns_success(self):
        response = self.client.get(
            reverse(
                "reservations:reservation_delete",
                kwargs={"titulo": self.reservation.titulo},
            )
        )

        self.assertEqual(response.status_code, 200)