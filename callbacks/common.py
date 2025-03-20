from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (
    ConversationHandler,
    ContextTypes
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:  # TODO wtf is cancel?? read about fallbacks
    await update.message.reply_text(
        "Something wrong :(\nSend /menu to see availible actions")
    return ConversationHandler.END

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    teacher_keyboard = [["/profile", "/groups"]]  # TODO add keys to all keyboards
    student_keyboard = [["/profile"]]
    if context.user_data.get('is_teacher'):
        kb_in_use = teacher_keyboard
    else:
        kb_in_use = student_keyboard
    await update.message.reply_text(
            "I'm here. Still waiting for some doog command."
            "Choose it from the keyboard menu.",
            reply_markup=ReplyKeyboardMarkup(kb_in_use, resize_keyboard=True, 
                                             one_time_keyboard=True, 
                                             input_field_placeholder='some action')
        )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello, {update.effective_user.first_name}!'
        ' Print /registration to sign up')