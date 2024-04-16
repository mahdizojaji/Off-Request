from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils import timezone

from core.models import OffRequest
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
                    "this_month_accepted_offs",
                    "this_season_accepted_offs",
                    "this_year_accepted_offs",
                )
            },
        ),
    )
    readonly_fields = (
        "this_month_accepted_offs",
        "this_season_accepted_offs",
        "this_year_accepted_offs",
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

    @admin.display(description="مرخصی های این ماه")
    def this_month_accepted_offs(self, obj: User):
        time_now = timezone.now()
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__year=time_now.year,
            off_at__month=time_now.month,
        ).count()

    @admin.display(description="مرخصی های این فصل")
    def this_season_accepted_offs(self, obj: User):
        time_now = timezone.now()
        current_season = (time_now.month - 1) // 3 + 1
        season_to_month_mapper = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__year=time_now.year,
            off_at__month__in=season_to_month_mapper[current_season],
        ).count()

    @admin.display(description="مرخصی های امسال")
    def this_year_accepted_offs(self, obj: User):
        time_now = timezone.now()
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__year=time_now.year,
        ).count()


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
