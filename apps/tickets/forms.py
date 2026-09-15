from django import forms
from .models import Ticket


class TicketForm(forms.ModelForm):

    class Meta:
        model = Ticket
        fields = ['titulo', 'descricao']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'campo-titulo',
                'placeholder': 'Titulo do chamado',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'campo-descricao',
                'placeholder': 'Descrição do chamado',
                'maxlength': '1500'}),
        }
