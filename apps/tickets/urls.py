from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
)


app_name = 'tickets'

urlpatterns = [
    path(
        '',
        TicketListView.as_view(),
        name='ticket_list',
    ),

    path(
        'create/',
        TicketCreateView.as_view(),
        name='ticket_create',
    ),

    path(
        'chamado/<str:titulo>',
        TicketDetailView.as_view(),
        name='ticket_detail',
    ),
]
