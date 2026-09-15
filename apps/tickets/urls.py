from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    TickerUpdateView,
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

    path(
        'chamado/<str:titulo>',
        TickerUpdateView.as_view(),
        name='ticket_update',
    )
]
