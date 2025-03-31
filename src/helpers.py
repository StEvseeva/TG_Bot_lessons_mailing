from telegram.ext import (
    ContextTypes
    )

from schemas import SGroupGet
from repository import UserRepository
from typing import List

yes_no_keyboard = [['yes', 'no']]

async def is_teacher(chat_id, context: ContextTypes.DEFAULT_TYPE) -> bool:
    if not 'is_teacher' in context.user_data:
        user = await UserRepository.get([chat_id])
        context.user_data['is_teacher'] = user[0].is_teacher if user else False
    if context.user_data['is_teacher']:
        return True
    return False

def pretty_teacher_groups(groups: List[SGroupGet], full: bool = False):
        text_groups = '\n'
        for group in groups:
            text_groups += f'{group.name} <b>|</b> {group.description}\n'
            if full:
                if group.students: # TODO tabs??????????????
                    for student in group.students:
                        student_str = student.surname + ' ' + student.name
                        text_groups += f'{student_str}\n'
                    text_groups += '\n'
                else:
                    text_groups += f'No students\n\n'
        return text_groups
