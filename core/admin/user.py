from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from jdatetime import datetime, date, j_days_in_month, timedelta

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
        time_now = datetime.now()
        first_day_of_month = date(year=time_now.year, month=time_now.month, day=1).togregorian()
        current_month_max_days = j_days_in_month[time_now.month - 1]
        latest_day_of_month = date(
            year=time_now.year, month=time_now.month, day=current_month_max_days
        ).togregorian()
        if time_now.isleap():
            latest_day_of_month += timedelta(days=1)
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__range=(first_day_of_month, latest_day_of_month),
        ).count()

    @admin.display(description="مرخصی های این فصل")
    def this_season_accepted_offs(self, obj: User):
        time_now = datetime.now()
        current_season = (time_now.month - 1) // 3 + 1
        season_to_month_mapper = {
            1: [1, 2, 3],
            2: [4, 5, 6],
            3: [7, 8, 9],
            4: [10, 11, 12],
        }
        first_day_of_season = date(
            year=time_now.year,
            month=season_to_month_mapper[current_season][0],
            day=1,
        ).togregorian()
        latest_season_month_max_days = j_days_in_month[season_to_month_mapper[current_season][-1]]
        latest_day_of_season = date(
            year=time_now.year,
            month=season_to_month_mapper[current_season][-1],
            day=latest_season_month_max_days,
        ).togregorian()
        if time_now.isleap():
            latest_day_of_season += timedelta(days=1)
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__range=(first_day_of_season, latest_day_of_season),
        ).count()

    @admin.display(description="مرخصی های امسال")
    def this_year_accepted_offs(self, obj: User):
        time_now = datetime.now()
        first_day_of_year = date(
            year=time_now.year,
            month=1,
            day=1,
        ).togregorian()
        latest_day_of_year = date(
            year=time_now.year,
            month=12,
            day=j_days_in_month[-1],
        ).togregorian()
        if time_now.isleap():
            latest_day_of_year += timedelta(days=1)
        return OffRequest.objects.filter(
            employee=obj,
            state=OffRequest.State.ACCEPTED,
            off_at__range=(first_day_of_year, latest_day_of_year),
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
