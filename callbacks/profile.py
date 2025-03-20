from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ContextTypes
    )

from repository import UserRepository
from schemas import SGroupGet

from typing import List

async def get_profile(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    def pretty_teacher_groups(groups: List[SGroupGet]):
        text_groups = '\n'
        for group in groups:
            text_groups += f'{group.name} <b>|</b> {group.description}\n'
        return text_groups

    def pretty_student_groups(groups: List[SGroupGet]):
        text_groups = '\n'
        for group in groups:
            text_groups += f'Teacher: {group.teacher_id} <b>|</b> {group.name}\n'
        return text_groups

    chat_id = update.message.chat_id
    user = await UserRepository.get(chat_id=chat_id)
    if not user:
        await update.message.reply_text(
        "You don't have a profile yet. Send /registration to create it.")
        return
    user = user[0]
    text = f"<b>Name</b>: {user.name}"
    text += f"\n<b>Surname</b>: {user.surname}"
    text += "\n\n<b>Groups</b>: " 
    if user.is_teacher:
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
    await update.message.reply_text(text)

# TODO add function for edit profile 