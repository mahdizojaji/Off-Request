from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models.user import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        "phone_number",
        "get_full_name",
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


# @admin.register(BaleMessengerUser)
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
