from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import BaleMessengerUser
from core.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "id",
        "phone_number",
        "first_name",
        "last_name",
        "is_staff",
    )
    list_filter = ("is_staff",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "groups",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone_number",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "groups",
                ),
            },
        ),
    )
    search_fields = (
        "phone_number",
        "first_name",
        "last_name",
    )
    ordering = ("id",)


@admin.register(BaleMessengerUser)
class BaleMessengerUserAdmin(admin.ModelAdmin):
    list_display = (
        "bale_id",
        "phone_number",
        "username",
    )
    fields = (
        "bale_id",
        "phone_number",
        "username",
        "first_name",
        "last_name",
        "created_at",
    )
    readonly_fields = (
        "bale_id",
        "phone_number",
        "username",
        "first_name",
        "last_name",
        "created_at",
    )
    search_fields = (
        "bale_id",
        "phone_number",
    )
