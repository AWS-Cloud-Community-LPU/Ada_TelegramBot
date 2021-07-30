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
from telegram import Update, ParseMode
import constants as C
import rss_feed as R

print("Bot Started...")
print(f"\n\nBot Started at {datetime.now()}\n", file=open(C.LOG_FILE, 'a+'))

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)


def get_time():
    """Gets Current Time
    Returns:
        HH:MM:SS AM/PM DD/MM/YYYY
    """
    return datetime.now().strftime('%I:%M:%S %p %d/%m/%Y')


def get_username(update: Update, context: CallbackContext):
    """Gets Username of a person
    Returns:
        username
    """
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    return username


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


def events_command(update: Update, context: CallbackContext) -> int:
    """Shows Upcoming events

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    try:
        with open(C.EVENT_STORE, "r") as event_file:
            line_events = event_file.readlines()
            line_length = len(line_events)
            if line_length == 0:
                update.message.reply_text(
                    C.NO_EVENTS, parse_mode=ParseMode.MARKDOWN)
                return -1
            for i in range(0, line_length, 2):
                line_event = line_events[i] + line_events[i+1]
                update.message.reply_text(
                    line_event, parse_mode=ParseMode.HTML)
            return 0
    except FileNotFoundError:
        update.message.reply_text(C.NO_EVENTS, parse_mode=ParseMode.MARKDOWN)
        return -2


def send_logs(update: Update, context: CallbackContext) -> None:
    """Sends Logs
    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    chat_id = update.message.chat_id
    username = get_username(update, context)
    print(f"Command: Get Logs", file=open(C.LOG_FILE, 'a+'))
    print(f"Time: {get_time()}", file=open(C.LOG_FILE, 'a+'))
    print(f"User: {username}", file=open(C.LOG_FILE, 'a+'))
    if username == "garvit_joshi9":  # Sent from Developer
        try:
            with open(C.LOG_FILE, "rb") as file:
                context.bot.send_document(
                    chat_id=chat_id, document=file, filename=C.LOG_FILE)
        except Exception as e:
            print(f"Remarks: Error with File logs",
                  file=open(C.LOG_FILE, 'a+'))
            print(f"{e}", file=open(C.LOG_FILE, 'a+'))
            update.message.reply_text("Error with logs file.")
    else:
        print("Remarks: Not a Developer", file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(
            "Sorry!! This command can only be executed by developer")
    print("", file=open(C.LOG_FILE, 'a+'))


def main():
    """Main function responsible for starting the bot and listening to commands.
    """
    # Create the Updater and pass it our bot's token.
    updater = Updater(keys.API_KEY, use_context=True, workers=5)

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
    dispatch.add_handler(CommandHandler(
        "get_logs", send_logs, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
