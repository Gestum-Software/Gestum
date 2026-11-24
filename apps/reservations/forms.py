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

            'inicio': forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                },
                format="%Y-%m-%dT%H:%M",
            ),

            'fim': forms.DateTimeInput(
                attrs={
                    "type": "datetime-local"
                },
                format="%Y-%m-%dT%H:%M",
            ),

            'resource': forms.Select(attrs={
                'class': 'campo-recursos',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["inicio"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["fim"].input_formats = ["%Y-%m-%dT%H:%M"]
