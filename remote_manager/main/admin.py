from django.contrib import admin
from .models import Organization, CustomUser


# Register your models here.
@admin.register(Organization, CustomUser)
class DefaultAdmin(admin.ModelAdmin):
    pass
