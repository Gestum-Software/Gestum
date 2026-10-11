from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import Group

User = get_user_model()


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'campo-nome',
            'placeholder': 'Digite o nome'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'campo-senha',
            'placeholder': 'Digite a senha'
        })


class CustomUserWithGroupsCreationForm(CustomUserCreationForm):

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={
            'class': 'campo-grupo'
        }),
        label='Selecione os perfis',
    )

    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit:
            user.groups.set(self.cleaned_data['groups'])
        else:
            old_save_m2m = self.save_m2m

            def new_save_m2m():
                old_save_m2m()
                user.groups.set(self.cleaned_data['groups'])
            self.save_m2m = new_save_m2m
        return user


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite seu usuário'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Digite sua senha'
    }))
