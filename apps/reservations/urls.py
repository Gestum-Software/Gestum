from django.urls import path
from .views import (
    ReservationListView,
    ReservationCreateView,
    ReservationDetailView,
)

app_name = 'reservations'

urlpatterns = [
    path(
        '',
        ReservationListView.as_view(),
        name='reservation_list',
    ),

    path(
        'create/',
        ReservationCreateView.as_view(),
        name='reservation_create',
    ),

    path(
        'reserva/<str:titulo>',
        ReservationDetailView.as_view(),
        name='reservation_detail',
    ),
]
