from django.conf import settings
from django.db import models
from django.db.models import ForeignKey


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class Favorite(models.Model):
    """Избранные."""
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    adv = ForeignKey(
        Advertisement,
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ('user', 'adv')