from balethon.objects import Message
from core.services.user import upsert_bale_user


class UserInfoHandler:
    def __call__(self, message: Message):
        self.message = message
        upsert_bale_user(
            bale_id=message.author.id,
            username=message.author.username,
            first_name=message.author.first_name,
            last_name=message.author.last_name,
        )
        self.send_user_info_message()

    def send_user_info_message(self):
        text = "آیدی شما: {}".format(self.message.author.id)
        self.message.reply(
            text=text,
        )
