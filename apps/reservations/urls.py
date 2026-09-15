from django.urls import path
from .views import (
    ReservationListView
)


urlpatterns = [
    path(
        '',
        ReservationListView.as_view(),
        name='reservation_list',
    ),
]
