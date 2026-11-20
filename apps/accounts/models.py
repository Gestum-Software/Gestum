from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

    def __str__(self):
        return self.username


class InitialAdminSetupLock(models.Model):
    id = models.PositiveSmallIntegerField(
        primary_key=True,
        default=1,
        editable=False,
    )
    revision = models.PositiveIntegerField(default=0)
