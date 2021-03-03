from string import Template
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
)
from telegram import Update
import api_key as keys
import constants as C


print("Bot Started...")

def start_command(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    update.message.reply_text(f'Hy there!! {user.first_name}')

def help_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(C.HELP_TEXT)

def source_command(update:Update, context: CallbackContext) -> None:
    username = update.message.from_user.first_name
    message = Template(C.SOURCE).substitute(name=username)
    update.message.reply_text(message)

def events_command(update:Update, context: CallbackContext) -> None:
    update.message.reply_text(C.EVENTS)

def main():
    # Create the Updater and pass it your bot's token.
    updater = Updater(keys.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(CommandHandler("start", start_command))
    dispatch.add_handler(CommandHandler("help", help_command))
    dispatch.add_handler(CommandHandler("source", source_command))
    dispatch.add_handler(CommandHandler("events", events_command))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
	# SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == "__main__":
    main()
