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

from db import create_table, delete_table, create_posts
from callbacks.registration import (
    CONFIRMATION_CODE, USER_ROLE, CREDENTIALS,
    registration_start,
    registration_end,
    registration_student,
    registration_teacher,
    check_conf_code
)
from callbacks.groups import (
    GROUP_NAME, GROUP_DESCRIPTION, STUDENTS_START, STUDENTS_LIST,
    GROUP_FORK, STUDENTS_FORK,
    add_students_start,
    add_students_list,
    add_students_end,
    add_group_fork,
    add_group_name,
    add_group_start,
    get_groups
)
from callbacks.common import cancel, start, menu
from callbacks.profile import get_profile

async def post_init(app: Application) -> None:
    # await delete_table()
    # await create_table()
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
    add_students_handler = ConversationHandler(
        entry_points=[CommandHandler("add_students", add_students_start)],
        states={
            STUDENTS_START: [
                CommandHandler("menu", menu),
                MessageHandler(filters.TEXT, add_students_start)
                ],
            STUDENTS_LIST: [MessageHandler(filters.TEXT, add_students_list)],
            STUDENTS_FORK: [
                MessageHandler(filters.Regex("^yes$"), add_students_start),
                MessageHandler(filters.Regex("^no$"), add_students_end)
                ],
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    add_group_handler = ConversationHandler(
        allow_reentry=True,
        entry_points=[CommandHandler("add_group", add_group_start)],
        states={
            GROUP_NAME: [MessageHandler(filters.TEXT, add_group_name)],
            GROUP_DESCRIPTION: [MessageHandler(filters.TEXT, add_group_fork)],
            GROUP_FORK: [
                add_students_handler,
                MessageHandler(filters.Regex("^done$"), menu)],
            STUDENTS_START: [CommandHandler("menu", menu)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    
    app.add_handler(reg_handler)
    app.add_handler(add_group_handler)
    app.add_handler(add_students_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("profile", get_profile))
    app.add_handler(CommandHandler("groups", get_groups))
    app.add_handler(CommandHandler("menu", menu))
    app.run_polling()


# TODO set sensetive settings (os and dotenv)
# TODO add SQLite
# TODO move handlers to handlers.py
# TODO add uvicorn?
# TODO move all constants
