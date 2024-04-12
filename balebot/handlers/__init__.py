from balethon import conditions
from balethon.event_handlers import MessageHandler

from balebot.handlers.start import StartHandler

HANDLERS = [
    MessageHandler(callback=StartHandler(), condition=(conditions.command("start"))),
]
