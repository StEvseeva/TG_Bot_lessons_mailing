import os

from loggers import get_logger
logger_main = get_logger(__name__)

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    Application,
    CommandHandler,
    ConversationHandler,
    MessageHandler,
    ContextTypes,
    filters
    )

from dotenv import load_dotenv

from db import create_table, delete_table
from schemas import STeacherAdd, SStudentAdd
from repository import TeacherRepository, StudentRepository

load_dotenv()

USER_TYPE, CONFIRMATION_CODE, CREDENTIALS = range(3)

async def registration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        'It\'s a function for registration. '
         'It\'s already done, but... <3')
    reply_keyboard = [["Teacher", "Student"]]
    await update.message.reply_text(
        "Are you a teacher or a student?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="teacher/student?"
        ),)
    return USER_TYPE

async def registration_teacher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['user_type'] = 'teacher'
    await update.message.reply_text(
    'Send me a confirmation code, please. '
    'If you don\'t have one, ask admin for it.')
    return CONFIRMATION_CODE

async def check_conf_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text
    # TODO: validate code
    await update.message.reply_text(
        f'Now send me your real name and (optional) surname.'
        ' Answer with only 2 words, please. Here is an example:\n\n'
        'Jules Ostin')
    return CREDENTIALS

async def registration_student(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['user_type'] = 'student'
    await update.message.reply_text(
        f'Oh, nice. I need to know, how can i call you.'
        ' What\'s your real name and surname? Answer with 1 or 2 words, please.')
    return CREDENTIALS

async def registration_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    creds = update.message.text.split()
    context.user_data['creds'] = creds
    if context.user_data['user_type'] == 'teacher':
        teacher = STeacherAdd(name=creds[0], chat_id=update.message.chat_id)
        if len(creds) > 1:
            teacher.surname = creds[1]
        await TeacherRepository.put(teacher)
    elif context.user_data['user_type'] == 'student':
        student = SStudentAdd(name=creds[0], surname=creds[1], chat_id=update.message.chat_id)
        await StudentRepository.put(student)
    await update.message.reply_text(
        f'Thank you for registration, {creds[0]}! See, what else you can do'
        ' by click on the button in the bottom of your device.')
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello, {update.effective_user.first_name}!'
        ' Print /registration to sign up')

async def create_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    pass


async def post_init(app: Application) -> None:
    await delete_table()
    await create_table()


if __name__ == '__main__':

    app = ApplicationBuilder().token(os.getenv('BOT_API_KEY')).post_init(post_init).build()
    reg_handler = ConversationHandler(
        entry_points=[CommandHandler("registration", registration)],
        states={
            USER_TYPE: [
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
    app.run_polling()


# TODO: set sensetive settings (os and dotenv)
# TODO: add SQLite
# TODO: move handlers to handlers.py
# TODO: add uvicorn?
# TODO: log in file instead of terminal
