from django.db import models


class Resource(models.Model):

    class StatusChoices(models.TextChoices):
        DISPONIVEL = 'disponivel', 'Disponível'
        EM_MANUTENCAO = 'manutencao', 'Em Manutenção'

    nome = models.CharField(max_length=50) 
    observacoes = models.TextField(max_length=1500, blank=False, null=False)
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.DISPONIVEL,
    )

    def __str__(self):
        return f"{self.nome} | ({self.status})"

    class Meta:
        permissions = [
            ('can_create_resources', 'Pode criar recursos'),
            ('can_delete_resources', 'Pode excluir recursos'),
            ('can_edit_resources', 'Pode editar recursos'),
        ]
