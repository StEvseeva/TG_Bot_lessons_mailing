from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
    )

from repository import UserRepository, GroupRepository
from schemas import SGroupBase
from loggers import get_logger

logger = get_logger(__name__)

NAME, DESCRIPTION, MENU = range(3)

async def add_group_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.debug(f'start add group | chat_id: \'{update.message.chat_id}\'')
    if not 'is_teacher' in context.user_data:
        user = await UserRepository.get(update.message.chat_id)
        context.user_data['is_teacher'] = user[0].is_teacher
    if context.user_data['is_teacher']:
        await update.message.reply_text(
            "<b>Set Name</b>\n\nThe name of the group will be displayed on your students' screens."
            " It's a public name, so choose something like: \n\n"
            "<i>'English 1A'</i> or <i>'Class Romashka'</i>\n"
            "The name of group may be in Russian or English."
        )
        return NAME
    else:
        await update.message.reply_text(
            "Sorry, you can't create own groups as a student :( \n\n"
            "P.S. How did you even find this page? It's a secret choice.\n"
            f"<i>You're a <s>wizard</s> hacker, user№{update.message.chat_id}.</i>",

        )
        return MENU# TODO exit to menu

async def add_group_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.chat_data['group_name']= update.message.text
    reply_keyboard = [["Skip"]]
    await update.message.reply_text(
            "<b>Set Description</b>\n\nThe description of the group is visible only for you."
            " It's an optional field, you can skip it.\n"
            "The description of group may be in Russian or English.",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, resize_keyboard=True, 
                                             one_time_keyboard=True)
        )
    return DESCRIPTION

async def add_group_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    desc = update.message.text
    group = SGroupBase(name=context.chat_data['group_name'], teacher_id=update.message.chat_id)
    if desc != 'Skip':
        group.description = desc
    group_id = await GroupRepository.put(group)
    await update.message.reply_text(
            f"Group '{group.name}' with id '{group_id}' was created.",
            reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END
    

async def add_patch_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass