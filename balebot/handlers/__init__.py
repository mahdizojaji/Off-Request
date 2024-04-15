from balethon import conditions
from balethon.event_handlers import MessageHandler, CallbackQueryHandler

from balebot.handlers.off_request import OffRequestHandler
from balebot.handlers.share_number import ShareNumberHandler
from balebot.handlers.start import StartHandler
from balebot.handlers.user_info import UserInfoHandler

HANDLERS = [
    MessageHandler(
        callback=StartHandler(),
        condition=(conditions.text & conditions.command("start")),
    ),
    MessageHandler(
        callback=UserInfoHandler(),
        condition=(conditions.text & conditions.command("info")),
    ),
    MessageHandler(
        callback=ShareNumberHandler(),
        condition=conditions.contact,
    ),
    CallbackQueryHandler(
        callback=OffRequestHandler(),
        condition=conditions.regex(r"^off-request-(.*)$"),
    ),
    CallbackQueryHandler(
        callback=StartHandler().call_back_query_wrapper,
        condition=conditions.regex(r"^back-home$"),
    ),
]
