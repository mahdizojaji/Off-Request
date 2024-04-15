from balethon.objects import (
    Message,
    ReplyKeyboard,
    ReplyKeyboardButton,
    InlineKeyboard,
    InlineKeyboardButton,
    CallbackQuery,
)
from django.utils.translation import gettext as _

from core.services.user import upsert_bale_user


class StartHandler:
    def __call__(self, message: Message):
        self.message = message
        user = upsert_bale_user(
            bale_id=message.author.id,
            username=message.author.username,
            first_name=message.author.first_name,
            last_name=message.author.last_name,
        )
        if user.phone_number and user.employee_profile:
            self.send_message_when_verified()
        else:
            self.send_message_when_not_verified()

    def call_back_query_wrapper(self, callback_query: CallbackQuery):
        callback_query.message.author = callback_query.author
        return self.__call__(callback_query.message)

    def send_message_when_verified(self):
        text = "به ربات ثبت مرخصی خوش آمدید.\n"
        text += "لطفا یکی از گزینه های زیر را انتخاب کنید."
        reply_markup = InlineKeyboard(
            [
                InlineKeyboardButton(
                    text=_("ثبت درخواست مرخصی"), callback_data="off-request-create"
                ),
            ],
        )
        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_when_not_verified(self):
        text = "به ربات ثبت مرخصی خوش آمدید.\n"
        text += "لطفا با کلیک بر روی دکمه ارسال شماره اقدام به احراز هویت نمایید."
        reply_markup = ReplyKeyboard(
            [
                ReplyKeyboardButton(_("ارسال شماره"), request_contact=True),
            ],
        )

        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )
