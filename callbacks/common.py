from telegram import Update
from telegram.ext import (
    ConversationHandler,
    ContextTypes
    )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    return ConversationHandler.END

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f'Hello, {update.effective_user.first_name}!'
        ' Print /registration to sign up')