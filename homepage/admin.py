from django.contrib import admin
from .models import Registration


@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "full_name",
        "email",
        "phone",
        "date_of_birth",
        "created_at",
    )

    search_fields = (
        "full_name",
        "email",
        "phone",
    )

    list_filter = (
        "created_at",
    )