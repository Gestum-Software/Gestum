from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView,
    TicketDetailView,
    TickerUpdateView,
    TicketDeleteView
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
        'update/<str:titulo>/',
        TickerUpdateView.as_view(),
        name='ticket_update',
    ),

    path(
        'delete/<str:titulo>/',
        TicketDeleteView.as_view(),
        name='ticket_delete'
    ),
]
