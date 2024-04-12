from balebot import bale_bot
from balebot.handlers import HANDLERS


def load_event_handlers():
    for handler in HANDLERS:
        bale_bot.add_event_handler(handler)
