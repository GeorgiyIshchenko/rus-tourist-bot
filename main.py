import logging
import os

from dotenv import load_dotenv

from telegram.ext import Application, CommandHandler, InlineQueryHandler, CallbackQueryHandler

from handlers import *

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

load_dotenv()

application = Application.builder().token(os.environ["BOT_TOKEN"]).build()

handlers = [
    CommandHandler("start", start),
    CommandHandler("help", help),
    CommandHandler("tours", tours),
    CommandHandler("routes", routes),
    CommandHandler("means_of_transport", means_of_transport),
    CommandHandler("advice", advice),
    CallbackQueryHandler(city_list, "category"),
    InlineQueryHandler(inline_query),
]
application.add_handlers(handlers)

application.run_polling(allowed_updates=Update.ALL_TYPES)

