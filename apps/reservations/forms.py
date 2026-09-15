from django import forms
from .models import Reservation


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['titulo', 'observacoes', 'inicio', 'fim', 'resource']
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'campo-titulo',
                'placeholder': 'Titulo da reserva',
            }),

            'observacoes': forms.Textarea(attrs={
                'class': 'campo-observacoes campo',
                'placeholder': 'Observações sobre o recurso',
                'maxlength': '1500'}),

            'inicio': forms.DateInput(attrs={
                'type': 'date',
            }),

            'fim': forms.DateInput(attrs={
                'type': 'date',
            }),

            'resource': forms.Select(attrs={
                'class': 'campo-recursos',
            }),
        }
