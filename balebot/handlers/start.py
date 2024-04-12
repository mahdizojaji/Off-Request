from balethon.objects import Message, ReplyKeyboard, ReplyKeyboardButton
from django.utils.translation import gettext as _

from core.services.user import upsert_bale_user


class StartHandler:
    def __call__(self, message: Message):
        self.message = message
        upsert_bale_user(
            bale_id=message.author.id,
            username=message.author.username,
            first_name=message.author.first_name,
            last_name=message.author.last_name,
        )
        self.send_message_to_sign_up()

    def send_message_to_sign_up(self):
        text = _("""
        Welcome to the bot.
        Please share your number by click the share number button.
        """)
        reply_markup = ReplyKeyboard(
            [
                ReplyKeyboardButton(_("Share number"), request_contact=True),
            ],
        )

        self.message.reply(
            text=text,
            reply_markup=reply_markup,
        )
