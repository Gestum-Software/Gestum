from django.conf import settings
from django.db import models
from apps.resources.models import Resource


class Reservation(models.Model):

    titulo = models.CharField(max_length=50)
    observacoes = models.TextField(max_length=1500, blank=False, null=False)
    inicio = models.DateTimeField()
    fim = models.DateTimeField()
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    resource = models.ForeignKey(
        Resource,
        on_delete=models.CASCADE,
    )

    def clean(self):
        super().clean()
        if self.inicio and self.fim and self.inicio >= self.fim:
            raise ValidationError(
                "A data de término deve ser posterior à data de início."
            )
