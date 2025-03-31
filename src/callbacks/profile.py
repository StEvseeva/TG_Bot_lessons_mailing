from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes
    )

from repository import UserRepository
from schemas import SGroupGet
from helpers import pretty_teacher_groups
from loggers import get_logger

from typing import List

logger = get_logger(__name__)

async def get_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    def pretty_student_groups(groups: List[SGroupGet]) -> str:
        text_groups = '\n'
        for group in groups:
            text_groups += f'Teacher: {group.teacher_chat_id} <b>|</b> {group.name}\n'
        return text_groups

    chat_id = update.message.chat_id
    user = await UserRepository.get(chat_ids=[chat_id])
    if not user:
        await update.message.reply_text(
        "You don't have a profile yet. Send /registration to create it.")
        return
    user = user[0]
    text = f"<b>Name</b>: {user.name}"
    text += f"\n<b>Surname</b>: {user.surname}"
    text += "\n\n<b>Groups</b>: " 
    kb_in_use = [['/menu']]
    if user.is_teacher:
        kb_in_use[0].append('/add_group')
        context.user_data['is_teacher'] = True
        if len(user.teacher_groups) > 0: # TODO check if may be just if user.teacher_groups:
            groups = f"{pretty_teacher_groups(user.teacher_groups)}"
        else:
            groups = "\nYou haven't added any groups yet"
    else:
        context.user_data['is_teacher'] = False
        if len(user.groups) > 0:
            groups = f"{pretty_student_groups(user.groups)}"
        else:
            groups = "\nYou haven't been added to any group yet"
    text += groups
    await update.message.reply_text(text,
                                    reply_markup=ReplyKeyboardMarkup(kb_in_use, resize_keyboard=True, 
                                             one_time_keyboard=True, 
                                             input_field_placeholder='some action'))

# TODO add /patch_description
# TODO add /add_groups