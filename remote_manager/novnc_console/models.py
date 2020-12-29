from django.db import models
from uuid import uuid4
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from main.models import Organization

# Create your models here.
class VNCSession(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=100,
        unique=True
    )

    ip4_addr = models.GenericIPAddressField(
        protocol='IPv4'
    )

    vnc_display = models.IntegerField(
        validators=[MaxValueValidator(10), MinValueValidator(1)]
    )

    password = models.CharField(
        max_length=50
    )

    organizations = models.ManyToManyField(
        Organization
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='vnc_created_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='vnc_updated_by')

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.name