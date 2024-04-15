from django.contrib import admin
from django.contrib.auth.models import Group

from .user import UserAdmin, BaleMessengerUserAdmin
from .off_request import OffRequestAdmin


admin.site.unregister(Group)


__all__ = [
    "UserAdmin",
    "BaleMessengerUserAdmin",
    "OffRequestAdmin",
]
