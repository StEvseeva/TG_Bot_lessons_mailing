import os
from dotenv import load_dotenv
load_dotenv()

from loggers import get_logger
logger_main = get_logger(__name__)

from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters
    )

from db import create_table, delete_table
from callbacks.registration import (
    CONFIRMATION_CODE, USER_ROLE, CREDENTIALS,
    registration,
    registration_end,
    registration_student,
    registration_teacher,
    check_conf_code
)
from callbacks.common import cancel, start
# from callbacks.profile import get_profile

async def post_init(app: Application) -> None:
    await delete_table()
    await create_table()


if __name__ == '__main__':

    app = ApplicationBuilder().token(os.getenv('BOT_API_KEY')).post_init(post_init).build()
    reg_handler = ConversationHandler(
        entry_points=[CommandHandler("registration", registration)],
        states={
            USER_ROLE: [
                MessageHandler(filters.Regex("^Teacher$"), registration_teacher),
                MessageHandler(filters.Regex("^Student$"), registration_student)
            ],
            CONFIRMATION_CODE: [MessageHandler(filters.TEXT, check_conf_code)],
            CREDENTIALS: [MessageHandler(filters.TEXT, registration_end)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(reg_handler)
    app.add_handler(CommandHandler("start", start))
    # app.add_handler(CommandHandler("profile", get_profile))
    app.run_polling()


# TODO: set sensetive settings (os and dotenv)
# TODO: add SQLite
# TODO: move handlers to handlers.py
# TODO: add uvicorn?
