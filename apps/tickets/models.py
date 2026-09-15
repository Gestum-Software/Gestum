from django.conf import settings
from django.db import models
from apps.resources.models import Resource


class Ticket(models.Model):

    class StatusChoices(models.TextChoices):
        ABERTO = 'aberto', 'Aberto'
        FINALIZADO = 'finalizado', 'Finalizado'

    titulo = models.CharField(max_length=50)
    descricao = models.TextField(max_length=1500, blank=False, null=False)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.ABERTO,
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='meus_modelos'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
    )
