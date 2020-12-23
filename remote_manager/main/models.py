from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

# Create your models here.
class Organization(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='group_created_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='group_updated_by'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.name



class CustomUser(AbstractUser):
    organization = models.ForeignKey(
        Organization,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    is_active = models.BooleanField(
        default=True,
    )

    is_staff = models.BooleanField(
        default=False,
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL,
        related_name='user_created_by'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        null=True
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_updated_by'

    )

    updated_at = models.DateTimeField(
        auto_now=True,
        null=True
    )

    def __str__(self):
        return self.username

