from django.urls import path
from .views import (
    ReservationListView,
    ReservationCreateView,
    ReservationDetailView,
    ReservationUpdateView,
    ReservationDeleteView,
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

    path(
        'update/<str:titulo>',
        ReservationUpdateView.as_view(),
        name='reservation_update',
    ),

    path(
        'delete/<str:titulo>',
        ReservationDeleteView.as_view(),
        name='reservation_delete',
    ),
]
