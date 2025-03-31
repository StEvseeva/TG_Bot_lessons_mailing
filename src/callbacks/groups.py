from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler
    )

from repository import GroupRepository, UserRepository
from helpers import is_teacher, pretty_teacher_groups, yes_no_keyboard
from schemas import SGroupBase, SGroupUpd
from loggers import get_logger

# TODO change add_students logic from message/command handlers to callback queries

logger = get_logger(__name__)

keyboard_students = [['/add_students', 'done']]
keuboard_groups = [['/add_group', '/patch_group'],['/menu']]

GROUP_NAME, GROUP_DESCRIPTION, GROUP_FORK, STUDENTS_START, STUDENTS_LIST, STUDENTS_FORK = range(6)

async def add_group_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    chat_id = update.message.chat_id
    logger.debug(f'start add group | chat_id: \'{chat_id}\'')
    if await is_teacher(chat_id, context):
        await update.message.reply_text(
            "<b>Set Name</b>\n\nThe name of the group will be displayed on your students' screens."
            " It's a public name, so choose something like: \n\n"
            "<i>'English 1A'</i> or <i>'Class Romashka'</i>\n"
            "The name of group may be in Russian or English.",
            reply_markup=ReplyKeyboardRemove()
        )
        return GROUP_NAME
    else:
        await update.message.reply_text(
            "Sorry, you can't create own groups as a student :( \n\n"
            "P.S. How did you even find this page? It's a secret choice.\n"
            f"<i>You're a <s>wizard</s> hacker, user№{chat_id}.</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        return STUDENTS_START

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
    return GROUP_DESCRIPTION

async def add_group_fork(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    desc = update.message.text
    group = SGroupBase(name=context.chat_data['group_name'], teacher_chat_id=update.message.chat_id)
    if desc != 'Skip':
        group.description = desc
    group_id = await GroupRepository.put(group)
    context.chat_data['group_id'] = group_id
    await update.message.reply_text(
            f"Group '{group.name}' with id '{group_id}' was created. If you want to add students in this group, press button",
            reply_markup=ReplyKeyboardMarkup(keyboard_students, resize_keyboard=True, 
                                             one_time_keyboard=True))
    return GROUP_FORK

async def add_group_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END
    

async def add_students_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not 'group_id' in context.chat_data:
        logger.warning('no group_id in context')
        await update.message.reply_text(
            f"Send me the name of group you want to add students in\n"
            "Example:\n\n First Group"
        )
        return STUDENTS_START
    await update.message.reply_text(
            f"Send me a list of users you'd like to add in this group. Users must be separeted by a space.\n"
            "Example:\n\n @user1 @user2"
        )
    return STUDENTS_LIST

async def add_students_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    students = map(int, update.message.text.split())
    for student in students:
        result = await UserRepository.add_to_group(student, context.chat_data['group_id'])
    await update.message.reply_text(
            f"Normalno. Dobavleno."
        )
    await update.message.reply_text(
            f"Do you want to add another students?", 
            reply_markup=ReplyKeyboardMarkup(yes_no_keyboard, resize_keyboard=True, 
                                             one_time_keyboard=True)
        )
    return STUDENTS_FORK

async def add_students_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
            f"Students have been added.",
            reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END

#TODO: add delete_students

async def get_groups(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not await is_teacher(update.message.chat_id, context):
        return
    groups = await GroupRepository.get_by_teacher_id(teacher_chat_id=update.message.chat_id)
    group_text = "\n\n<b>Groups</b>: "
    group_text += pretty_teacher_groups(groups, full=True)
    await update.message.reply_text(
        group_text,
        reply_markup=ReplyKeyboardMarkup(keuboard_groups, resize_keyboard=True, 
                                         one_time_keyboard=True))

async def patch_group(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    pass