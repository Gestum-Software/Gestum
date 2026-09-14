from django.views.generic.list import ListView
from .models import Ticket


class TicketListView(ListView):
    model = Ticket
