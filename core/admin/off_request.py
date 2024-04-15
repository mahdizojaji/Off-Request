from django.contrib import admin

from core.models import OffRequest


# @admin.register(OffRequest)
class OffRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "state",
        "off_at",
        "employee_full_name",
        "employee_phone_number",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "id",
                    "state",
                    "employee",
                    "off_at",
                    "reject_reason",
                )
            },
        ),
    )
    readonly_fields = (
        "id",
        "employee",
        "off_at",
    )
    add_fieldsets = (
        (
            None,
            {
                "fields": (
                    "state",
                    "off_at",
                    "employee",
                )
            },
        ),
    )
    add_readonly_fields = ()
    search_fields = (
        "id",
        "employee__id",
        "employee__phone_number",
    )
    list_filter = (
        "state",
        "off_at",
        "created_at",
    )

    @admin.display
    def employee_phone_number(self, obj: OffRequest):
        return f"{obj.employee.phone_number}"

    @admin.display
    def employee_full_name(self, obj: OffRequest):
        return f"{obj.employee.get_full_name()}"

    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets
        return super().get_fieldsets(request, obj)

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.add_readonly_fields
        return super().get_readonly_fields(request, obj)
