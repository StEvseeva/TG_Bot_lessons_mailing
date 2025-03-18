from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ConversationHandler,
    ContextTypes
    )

from repository import StudentRepository, TeacherRepository
from schemas import SStudentAdd, STeacherAdd

USER_ROLE, CONFIRMATION_CODE, CREDENTIALS = range(3)

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
    return USER_ROLE

async def registration_teacher(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['user_role'] = 'teacher'
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
    context.user_data['user_role'] = 'student'
    await update.message.reply_text(
        f'Oh, nice. I need to know, how can i call you.'
        ' What\'s your real name and surname? Answer with only 2 words, please.')
    return CREDENTIALS

async def registration_end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    creds = update.message.text.split()
    context.user_data['creds'] = creds
    if context.user_data['user_role'] == 'teacher':
        teacher = STeacherAdd(name=creds[0], surname=creds[1], chat_id=update.message.chat_id)
        await TeacherRepository.put(teacher)
    elif context.user_data['user_role'] == 'student':
        student = SStudentAdd(name=creds[0], surname=creds[1], chat_id=update.message.chat_id)
        await StudentRepository.put(student)
    await update.message.reply_text(
        f'Thank you for registration, {creds[0]}! See, what else you can do'
        ' by click on the button in the bottom of your device.')
    return ConversationHandler.END