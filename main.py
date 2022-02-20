"""
MIT License
Copyright (c) 2022 AWS Cloud Community LPU
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


from string import Template
import configparser
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
)
from telegram import Update
import constants as C
import functions as F


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
        log_text = f"Welcome user at {F.get_time()} \nUser: {F.get_username(update, context)}\n"
        F.print_logs(log_text)


def start_command(update: Update, context: CallbackContext) -> None:
    """Start Command for Ada

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    user = update.message.from_user
    update.message.reply_text(f"Hy there !! {user.first_name}")


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


def send_logs(update: Update, context: CallbackContext) -> None:
    """Sends Logs

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    chat_id = update.message.chat_id
    username = F.get_username(update, context)
    log_text = "Command: Get Logs\n"
    log_text = log_text + f"Time: {F.get_time()}\n"
    log_text = log_text + f"User: {username}\n"
    if username == "garvit_joshi9":  # Sent from Developer
        try:
            with open(C.LOG_FILE, "rb") as file:
                context.bot.send_document(
                    chat_id=chat_id, document=file, filename=C.LOG_FILE
                )
        except Exception as err:
            log_text = log_text + "Remarks: Error with File logs\n"
            log_text = log_text + f"{err}\n"
            update.message.reply_text("Error with logs file.")
    else:
        log_text = log_text + "Remarks: Not a Developer\n"
        update.message.reply_text(C.ERROR_OWNER)
    F.print_logs(log_text)


def main():
    """Main function responsible for starting the bot and listening to commands."""
    config = configparser.ConfigParser()
    config.read("secrets.ini")

    # Create the Updater and pass it our bot's token.
    updater = Updater(token=config["KEYS"]["API_KEY"], use_context=True, workers=30)

    # Get the dispatcher to register handlers
    dispatch = updater.dispatcher

    # on different commands - answer in Telegram
    dispatch.add_handler(
        MessageHandler(Filters.status_update.new_chat_members, welcome_user)
    )
    dispatch.add_handler(CommandHandler("start", start_command))
    dispatch.add_handler(CommandHandler("help", help_command))
    dispatch.add_handler(CommandHandler("source", source_command))
    dispatch.add_handler(CommandHandler("events", F.events_command))
    dispatch.add_handler(CommandHandler("news", F.random_news))
    dispatch.add_handler(CommandHandler("brod_news", F.brodcast_news, run_async=True))
    dispatch.add_handler(CommandHandler("get_logs", send_logs, run_async=True))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    start_text = f"Bot Started at {F.get_time()}\n"
    F.print_logs(start_text, True)
    main()
