from re import search as re_search

from balethon.objects import (
    InlineKeyboard,
    InlineKeyboardButton,
    CallbackQuery,
    ReplyKeyboardRemove,
)
from django.conf import settings
from django.utils.translation import gettext as _
from jdatetime import date, datetime, j_days_in_month, FA_LOCALE

from core.models import BaleMessengerUser, OffRequest
from core.services.off_request import (
    get_or_create_temp_off_request,
    set_off_request_date,
    accept_off_request,
    reject_off_request,
)


class OffRequestHandler:
    SELECT_MONTH_CALLBACK_DATA_PATTERN = (
        r"^off-request-(?P<off_request_id>\d+)-month-(?P<month_number>\d+)$"
    )
    SELECT_DAY_CALLBACK_DATA_PATTERN = (
        r"^off-request-(?P<off_request_id>\d+)-month-(?P<month_number>\d+)-"
        r"day-(?P<day_number>\d+)$"
    )
    ACCEPT_OFF_REQUEST_CALLBACK_DATA_PATTERN = r"^off-request-(?P<off_request_id>\d+)-accept$"
    REJECT_OFF_REQUEST_CALLBACK_DATA_PATTERN = r"^off-request-(?P<off_request_id>\d+)-reject$"

    def __call__(self, callback_query: CallbackQuery):
        self.callback_query = callback_query
        if callback_query.data == "off-request-create":
            bale_user = BaleMessengerUser.objects.get(bale_id=callback_query.author.id)
            off_request = get_or_create_temp_off_request(bale_user.employee_profile_id)
            self.send_message_to_select_month(off_request.id)
        elif regex := re_search(self.SELECT_MONTH_CALLBACK_DATA_PATTERN, callback_query.data):
            self.regex = regex
            self.send_message_to_select_day()
        elif regex := re_search(self.SELECT_DAY_CALLBACK_DATA_PATTERN, callback_query.data):
            self.regex = regex
            off_request_id = int(self.regex.group("off_request_id"))
            month_number = int(self.regex.group("month_number"))
            day_number = int(self.regex.group("day_number"))
            off_request = set_off_request_date(
                off_request_id=off_request_id,
                off_date=date(
                    year=datetime.now().year, month=month_number, day=day_number
                ).togregorian(),
            )
            self.send_message_to_employer_check_request(off_request)
            self.send_message_for_waiting_employer()
        elif regex := re_search(self.ACCEPT_OFF_REQUEST_CALLBACK_DATA_PATTERN, callback_query.data):
            self.regex = regex
            off_request_id = int(self.regex.group("off_request_id"))
            off_request = accept_off_request(off_request_id=off_request_id)
            self.send_message_to_employer_to_confirm_request_status(off_request)
            self.send_message_to_inform_employee_from_request_status(off_request)
        elif regex := re_search(self.REJECT_OFF_REQUEST_CALLBACK_DATA_PATTERN, callback_query.data):
            self.regex = regex
            off_request_id = int(self.regex.group("off_request_id"))
            off_request = reject_off_request(off_request_id=off_request_id)
            self.send_message_to_employer_to_confirm_request_status(off_request)
            self.send_message_to_inform_employee_from_request_status(off_request)

    def send_message_to_select_month(self, off_request_id):
        text = "لطفا ماه مرخصی خود را انتخاب کنید."
        reply_markup = InlineKeyboard()
        available_month_counter = 0
        for month_number, month_name in enumerate(date.j_months_fa):
            if (month_number + 1) >= datetime.now().month:
                if available_month_counter % 2 == 0:
                    reply_markup.add_row()
                reply_markup.add_button(
                    InlineKeyboardButton(
                        text=month_name,
                        callback_data=f"off-request-{off_request_id}-month-{month_number + 1}",
                    ),
                    row_index=available_month_counter // 2,
                )
                available_month_counter += 1
        reply_markup.add_row(
            InlineKeyboardButton(
                text=_("بازگشت به منوی اصلی"),
                callback_data="back-home",
            )
        )
        self.callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_to_select_day(self):
        text = "لطفا روز مرخصی خود را انتخاب کنید."
        month_number = int(self.regex.group("month_number"))
        datetime_now = datetime.now()
        reply_markup = InlineKeyboard()
        day_counter = 0
        for day in range(1, j_days_in_month[month_number - 1] + 1):
            if (
                day > datetime.now().day and month_number == datetime_now.month
            ) or month_number > datetime_now.month:
                if day_counter % 2 == 0:
                    reply_markup.add_row()
                reply_markup.add_button(
                    InlineKeyboardButton(
                        text=f"{day}",
                        callback_data=f"{self.callback_query.data}-day-{day}",
                    ),
                    row_index=day_counter // 2,
                )
                day_counter += 1
        reply_markup.add_row(
            InlineKeyboardButton(
                text=_("بازگشت به منوی اصلی"),
                callback_data="back-home",
            )
        )
        self.callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_for_waiting_employer(self):
        month_number = int(self.regex.group("month_number"))
        month_name = date.j_months_fa[month_number - 1]
        day_number = int(self.regex.group("day_number"))
        text = "درخواست مرخصی شما برای {0} {1} به کارفرما ارسال شد.\n".format(
            day_number, month_name
        )
        text += "پس از بررسی نتیجه ي آن به شما اطلاع داده خواهد شد."
        reply_markup = InlineKeyboard(
            [
                InlineKeyboardButton(
                    text=_("بازگشت به منوی اصلی"),
                    callback_data="back-home",
                ),
            ],
        )
        self.callback_query.message.edit_text(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_to_employer_check_request(self, off_request: OffRequest):
        employee_name = off_request.employee.get_full_name()
        off_date = date.fromgregorian(date=off_request.off_at, locale=FA_LOCALE).strftime("%d %b")
        text = "یک درخواست مرخصی از {0} برای {1} ثبت شده است.\n".format(employee_name, off_date)
        text += "با کلیک بر روی یکی از دکمه های زیر آن را تایید یا رد کنید."
        reply_markup = InlineKeyboard()
        reply_markup.add_row(
            InlineKeyboardButton(
                text="تایید",
                callback_data=f"off-request-{off_request.id}-accept",
            ),
            InlineKeyboardButton(
                text="رد",
                callback_data=f"off-request-{off_request.id}-reject",
            ),
        )
        self.callback_query.client.send_message(
            chat_id=settings.EMPLOYER_BALE_ID,
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_to_employer_to_confirm_request_status(self, off_request: OffRequest):
        text = "وضعیت  درخواست با شناسه {} از {} موفقیت به {} تغییر پیدا کرد.".format(
            off_request.id,
            off_request.employee.get_full_name(),
            off_request.get_state_display(),
        )
        self.callback_query.message.edit_text(
            text=text,
            reply_markup=ReplyKeyboardRemove(),
        )

    def send_message_to_inform_employee_from_request_status(self, off_request: OffRequest):
        off_date = date.fromgregorian(date=off_request.off_at, locale=FA_LOCALE).strftime("%d %b")
        text = "درخواست مرخصی {} به وضعیت {} تغییر پیدا کرد.".format(
            off_date, off_request.get_state_display()
        )
        self.callback_query.client.send_message(
            chat_id=off_request.employee.bale_profile.bale_id,
            text=text,
            reply_markup=ReplyKeyboardRemove(),
        )
