from django.urls import path
from .views import (
    ReservationListView,
    ReservationCreateView,
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

]
