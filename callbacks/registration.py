from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    ContextTypes
    )

from repository import UserRepository
from schemas import SUserBase
from loggers import get_logger

logger = get_logger(__name__)

USER_ROLE, CONFIRMATION_CODE, CREDENTIALS = range(3)

async def registration_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug(f'start registration | chat_id: \'{update.message.chat_id}\'')
    reply_keyboard = [["Teacher", "Student"]]
    if await UserRepository.get(update.message.chat_id):
        await update.message.reply_text(
            "You already have a profile. Send /profile to take a look on you credentials."
            )
        return
    await update.message.reply_text(
        "Are you a teacher or a student?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="teacher/student?"
        ),)
    return USER_ROLE

async def registration_teacher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['is_teacher'] = True
    await update.message.reply_text(
    'Send me a confirmation code, please. '
    'If you don\'t have one, ask admin for it.')
    return CONFIRMATION_CODE

async def check_conf_code(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    code = update.message.text
    # TODO validate code
    await update.message.reply_text(
        f'Now send me your real name and (optional) surname.'
        ' Answer with only 2 words, please. Here is an example:\n\n'
        'Jules Ostin')
    return CREDENTIALS

async def registration_student(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['is_teacher'] = False
    await update.message.reply_text(
        f'Oh, nice. I need to know, how can i call you.'
        ' What\'s your real name and surname? Answer with only 2 words, please.')
    return CREDENTIALS

async def registration_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    creds = update.message.text.split()
    context.user_data['creds'] = creds
    user = SUserBase(name=creds[0], surname=creds[1], chat_id=update.message.chat_id)
    if context.user_data['is_teacher']:
        user.is_teacher = True   
    await UserRepository.put(user)
    await update.message.reply_text(
        f'Thank you for registration, {creds[0]}! See, what else you can do'
        ' by send /menu')
    logger.debug('end registration')
    return ConversationHandler.END