from string import Template
import secrets as keys
import logging
from datetime import datetime
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters
)
from telegram import Update
import constants as C
import rss_feed as R

print("Bot Started...")
print("\n\n\nBot Started at", datetime.now(), file=open(C.LOG_FILE, 'a+'))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def welcome_user(update: Update, context: CallbackContext) -> None:
    """Welcome Command for New User

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    for new_user in update.message.new_chat_members:
        chat_id = update.message.chat_id
        new_user = new_user.first_name
        welcome_message = "Welcome " + new_user
        context.bot.send_message(chat_id, welcome_message)
        print(f"Welcome user at {datetime.now()} User: {new_user}", file=open(
            C.LOG_FILE, 'a+'))


def start_command(update: Update, context: CallbackContext) -> None:
    """Start Command for Ada

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    user = update.message.from_user
    update.message.reply_text(f'Hy there !! {user.first_name}')


def help_command(update: Update, context: CallbackContext) -> None:
    """Help Command for User

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    update.message.reply_text(C.HELP_TEXT)


def source_command(update: Update, context: CallbackContext) -> None:
    """Prints GitHub Source Code

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    username = update.message.from_user.first_name
    message = Template(C.SOURCE).substitute(name=username)
    update.message.reply_text(message)


def events_command(update: Update, context: CallbackContext) -> None:
    """Shows Upcoming events

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    update.message.reply_text(C.EVENTS)


def main():
    """Main function responsible for starting the bot and listening to commands.
    """
    # Create the Updater and pass it our bot's token.
    updater = Updater(keys.API_KEY, use_context=True)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(MessageHandler(
        Filters.status_update.new_chat_members, welcome_user))
    dispatch.add_handler(CommandHandler("start", start_command))
    dispatch.add_handler(CommandHandler("help", help_command))
    dispatch.add_handler(CommandHandler("source", source_command))
    dispatch.add_handler(CommandHandler("events", events_command))
    dispatch.add_handler(CommandHandler("news", R.random_news))
    dispatch.add_handler(CommandHandler(
        "brod_news", R.brodcast_news, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
