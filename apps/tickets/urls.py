from django.urls import path
from .views import (
    TicketListView
)


app_name = 'tickets'

urlpatterns = [
    path(
        '',
        TicketListView.as_view(),
        name='tickets_list'
    ),
]
