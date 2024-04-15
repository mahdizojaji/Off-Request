from balethon.objects import (
    Message,
    ReplyKeyboard,
    ReplyKeyboardButton,
    ReplyKeyboardRemove,
    InlineKeyboard,
    InlineKeyboardButton,
)
from django.utils.translation import gettext as _

from core.services.user import (
    is_employee,
    update_bale_user_phone_number,
    link_bale_user_to_employee,
)


class ShareNumberHandler:
    def __call__(self, message: Message):
        self.message = message
        if message.author.id != message.contact.user_id:
            self.send_message_when_not_own_number()
        elif not is_employee(message.contact.phone_number):
            update_bale_user_phone_number(message.contact.user_id, message.contact.phone_number)
            self.send_message_when_is_not_employee()
        else:
            update_bale_user_phone_number(message.contact.user_id, message.contact.phone_number)
            link_bale_user_to_employee(message.contact.phone_number)
            self.send_message_when_verified()

    def send_message_when_not_own_number(self):
        text = "\nاین شماره متعلق به اکانت شما نیست."
        text += "لطفا شماره معتبر را با کلیک بر روی دکمه ارسال شماره ارسال کنید."
        reply_markup = ReplyKeyboard(
            [
                ReplyKeyboardButton(_("ارسال شماره"), request_contact=True),
            ],
        )
        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_when_is_not_employee(self):
        text = "متاسفانه شماره شما به عنوان کارمند ثبت نشده است."
        reply_markup = ReplyKeyboardRemove()
        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )

    def send_message_when_verified(self):
        text = "لطفا یکی از گزینه های زیر را انتخاب کنید."
        reply_markup = InlineKeyboard(
            [
                InlineKeyboardButton(
                    text=_("ثبت درخواست مرخصی"),
                    callback_data="off-request-create",
                ),
            ],
        )
        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )
