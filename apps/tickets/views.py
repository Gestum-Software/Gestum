from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from .models import Ticket
from .forms import TicketForm


class TicketListView(ListView):
    model = Ticket


class TicketCreateView(CreateView):
    model = Ticket
    form_class = TicketForm
    success_url = 'chamados/'
