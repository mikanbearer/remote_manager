from django.contrib import admin
from .models import VNCSession


# Register your models here.
@admin.register(VNCSession)
class DefaultAdmin(admin.ModelAdmin):
    pass