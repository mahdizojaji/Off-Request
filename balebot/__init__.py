from django.conf import settings

from balethon import Client

bale_bot = Client(settings.BALETHON["BALE_BOT_TOKEN"])


__all__ = ["bale_bot"]
