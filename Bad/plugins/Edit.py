from telegram import Update, Message
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from telegram.constants import ParseMode
from Bad import application

# Global toggle variable
EDITTEXT_DELETE_ENABLED = True

# Handler to toggle the edittext mode
async def toggle_edittext(update: Update, context: CallbackContext):
    global EDITTEXT_DELETE_ENABLED
    args = context.args

    if not args:
        return await update.message.reply_text("❖ Usage: <code>/edittext on</code> or <code>/edittext off</code>", parse_mode=ParseMode.HTML)

    command = args[0].lower()
    if command == "on":
        EDITTEXT_DELETE_ENABLED = True
        await update.message.reply_text("✅ Edit & long message deletion has been <b>enabled</b>.", parse_mode=ParseMode.HTML)
    elif command == "off":
        EDITTEXT_DELETE_ENABLED = False
        await update.message.reply_text("❌ Edit & long message deletion has been <b>disabled</b>.", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("❖ Invalid option.\nUse <code>/edittext on</code> or <code>/edittext off</code>.", parse_mode=ParseMode.HTML)

# Handle edited messages
async def handle_edited_message(update: Update, context: CallbackContext):
    if not EDITTEXT_DELETE_ENABLED:
        return

    edited_message = update.edited_message
    if edited_message:
        chat_id = edited_message.chat_id
        message_id = edited_message.message_id
        user = edited_message.from_user

        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            warning_text = f"⚠️ {user.mention_html()}, editing messages is not allowed."
            await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"[EDIT DELETE ERROR] {e}")

# Handle long messages
async def handle_long_message(update: Update, context: CallbackContext):
    if not EDITTEXT_DELETE_ENABLED:
        return

    message: Message = update.message
    if message and message.text and len(message.text.split()) > 60:
        try:
            chat_id = message.chat_id
            message_id = message.message_id
            user = message.from_user

            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            warning_text = f"⚠️ {user.mention_html()}, ʏᴏᴜʀ ᴍᴇꜱꜱᴀɢᴇ ᴇxᴄᴇᴇᴅꜱ 60 ᴡᴏʀᴅꜱ ᴀɴᴅ ʜᴀꜱ ʙᴇᴇɴ ᴅᴇʟᴇᴛᴇᴅ."
            await context.bot.send_message(chat_id=chat_id, text=warning_text, parse_mode=ParseMode.HTML)
        except Exception as e:
            print(f"[LONG DELETE ERROR] {e}")

# Register handlers
app_instance = application
app_instance.add_handler(CommandHandler("edittext", toggle_edittext))
app_instance.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_long_message))
app_instance.add_handler(MessageHandler(filters.ALL & filters.UpdateType.EDITED, handle_edited_message))