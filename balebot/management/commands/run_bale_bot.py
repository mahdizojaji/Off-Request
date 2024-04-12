from django.core.management.base import BaseCommand

from balebot import bale_bot
from balebot.services.handlers import load_event_handlers
from balebot.services.listener import run_with_long_polling


class Command(BaseCommand):
    help = "Start Bale bot"

    def handle(self, *args, **options):
        load_event_handlers()
        run_with_long_polling(bale_bot)
