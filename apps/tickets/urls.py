from django.urls import path
from .views import (
    TicketListView,
    TickerCreateView
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
        TickerCreateView.as_view(),
        name='tickets_create'
    ),
]
