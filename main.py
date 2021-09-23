from string import Template
import secrets as keys
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


def get_time(update: Update = None):
    """Gets Current Time

    Returns:
        HH:MM:SS {AM/PM} DD/MM/YYYY
    """
    if update is None:
        return datetime.now().strftime('%I:%M:%S %p %d/%m/%Y')
    return update.message.date.astimezone().strftime('%I:%M:%S %p %d/%m/%Y')


def get_username(update: Update, context: CallbackContext):
    """Gets Username of a person

    Returns:
        username
    """
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    if username is None:
        username = context.bot.getChatMember(chat_id, user_id).user.full_name
        username = username + "(Name)"
    return username


def print_logs(log_message):
    """Writes logs in logs.txt
    """
    line = "-------------\n"
    log_message = line + log_message + line
    with open(C.LOG_FILE, 'a+', encoding='utf8') as log_file:
        print(log_message, file=log_file)


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
        log_text = f"Welcome user at {get_time()} \nUser: {get_username(update, context)}\n"
        print_logs(log_text)


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
        log_text = f"Command: {get_username(update, context)}\n"
        log_text = log_text + f"User: {get_username(update, context)}\n"
        print_logs(log_text)
        with open(C.EVENT_STORE, "r", encoding="utf-8") as event_file:
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
    log_text = "Command: Get Logs\n"
    log_text = log_text + f"Time: {get_time()}\n"
    log_text = log_text + f"User: {username}\n"
    if username == "garvit_joshi9":  # Sent from Developer
        try:
            with open(C.LOG_FILE, "rb") as file:
                context.bot.send_document(
                    chat_id=chat_id, document=file, filename=C.LOG_FILE)
        except Exception as e:
            log_text = log_text + "Remarks: Error with File logs\n"
            log_text = log_text + f"{e}\n"
            update.message.reply_text("Error with logs file.")
    else:
        log_text = log_text + "Remarks: Not a Developer\n"
        update.message.reply_text(C.ERROR_OWNER)
    print_logs(log_text)


def main():
    """Main function responsible for starting the bot and listening to commands.
    """
    # Create the Updater and pass it our bot's token.
    updater = Updater(keys.API_KEY, use_context=True, workers=30)

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
    dispatch.add_handler(CommandHandler("get_logs", send_logs, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    start_text = f"Bot Started at {get_time()}\n"
    print(start_text)
    print_logs(start_text)
    main()
