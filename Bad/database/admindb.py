from telegram import Update
from telegram.ext import CallbackContext

async def admin_check(update: Update, context: CallbackContext) -> bool:
    message = update.message
    if not message.from_user:
        return False

    if message.chat.type not in ["supergroup", "channel"]:
        return False

    if message.from_user.id in [
        777000,  # Telegram Service Notifications
        7436017266,  # bot
    ]:
        return True

    chat_id = message.chat.id
    user_id = message.from_user.id

    member = await context.bot.get_chat_member(chat_id=chat_id, user_id=user_id)
    if member.status not in ["administrator", "creator"]:
        return False
    else:
        return True
      
