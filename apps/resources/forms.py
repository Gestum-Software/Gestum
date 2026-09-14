from django import forms
from .models import Resource


class ResourceForm(forms.ModelForm):

    class Meta:
        model = Resource
        fields = ['nome', 'observacoes']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'campo-nome',
                'placeholder': 'Nome do recurso',
            }),

            'observacoes': forms.Textarea(attrs={
                'class': 'campo-observacoes campo',
                'placeholder': 'Observações sobre o recurso',
                'maxlength': '1500'}),
        }
