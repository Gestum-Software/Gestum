from django.urls import path
from .views import (
    TicketListView,
    TicketCreateView
)


app_name = 'tickets'

urlpatterns = [
    path(
        '',
        TicketListView.as_view(),
        name='tickets_list'
    ),

    path(
        'create/',
        TicketCreateView.as_view(),
        name='tickets_create'
    ),
]
