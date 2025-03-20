import os
from dotenv import load_dotenv
load_dotenv()

from loggers import get_logger
logger_main = get_logger(__name__)

import telegram
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    filters,
    Defaults
    )

from db import create_table, delete_table
from callbacks.registration import (
    CONFIRMATION_CODE, USER_ROLE, CREDENTIALS,
    registration_start,
    registration_end,
    registration_student,
    registration_teacher,
    check_conf_code
)
from callbacks.groups import (
    NAME, DESCRIPTION, MENU,
    add_group_end,
    add_group_name,
    add_group_start
)
from callbacks.common import cancel, start, menu
from callbacks.profile import get_profile

async def post_init(app: Application) -> None:
    await delete_table()
    await create_table()
    pass


if __name__ == '__main__':


    defaults = Defaults(parse_mode=telegram.constants.ParseMode.HTML)
    app = ApplicationBuilder().token(
        os.getenv('BOT_API_KEY')
        ).post_init(post_init).defaults(defaults).build()
    

    reg_handler = ConversationHandler(
        entry_points=[CommandHandler("registration", registration_start)],
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
    add_group_handler = ConversationHandler(
        entry_points=[CommandHandler("add_group", add_group_start)],
        states={
            NAME: [MessageHandler(filters.TEXT, add_group_name)],
            DESCRIPTION: [MessageHandler(filters.TEXT, add_group_end)],
            MENU: [MessageHandler(filters.TEXT, menu)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    app.add_handler(reg_handler)
    app.add_handler(add_group_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", get_profile))
    app.add_handler(CommandHandler("menu", menu))
    app.run_polling()


# TODO set sensetive settings (os and dotenv)
# TODO add SQLite
# TODO move handlers to handlers.py
# TODO add uvicorn?
# TODO move all constants
