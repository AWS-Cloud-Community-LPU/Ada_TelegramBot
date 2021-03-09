import re
from datetime import datetime
import time
import secrets as keys
import random
import feedparser
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C


def check_status(update: Update, context: CallbackContext) -> int:
    """Checks status if brodcast news was sent from owner of group and from
    a perticular group.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    print(f"Brodcast News at: {datetime.now()}", file=open(
        C.LOG_FILE, 'a+'))
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the group
    user_status = context.bot.getChatMember(chat_id, user_id).status
    # user_status contains ("creator", "administrator" or "member")
    if str(chat_id) == keys.CHANNEL_ID:
        print("Test Case #1: Success", file=open(C.LOG_FILE, 'a+'))
    else:
        print("Test Case #1: FAILED\nChat ID:",
              chat_id, file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.ERROR_CHAT_ID,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1
    if user_status == "creator":
        print("Test Case #2: Success", file=open(C.LOG_FILE, 'a+'))
    else:
        print("Test Case #2: FAILED\nUser ID:",
              user_id, file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.ERROR_OWNER,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1
    return 0


def message_creator(entry) -> str:
    """Returns news in a proper format

    Keyword arguments:
        entry : a perticular entry of rss feed used for extracting data.
    """
    title = "<b>Title: " + entry.title + "</b>"
    cleanr = re.compile(
        '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    summary = re.sub(cleanr, '', entry.summary)
    summary = "\n\n<b>Summary:</b> " + summary
    link = "\n\n<b>Link: </b>" + "<a href=\"" + entry.link + "\">Click here</a>"
    message = title + summary + link
    return message


def brodcast_news(update: Update, context: CallbackContext):
    """Brodcasts news at 9:00am and 9:00pm everyday.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    if check_status(update, context) == -1:
        return -1
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    for entry in news_feed.entries:
        while True:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            time.sleep(1)
            if str(current_time) in ("09:01:00", "09:00:01"):
                message = message_creator(entry)
                context.bot.send_message(keys.CHANNEL_ID, message,
                                         parse_mode=ParseMode.HTML
                                         )
                print("News Message send at: ", now,
                      file=open(C.LOG_FILE, 'a+'))
                time.sleep(1)
            if str(current_time) in ("21:00:00", "21:00:01"):
                message = message_creator(entry)
                context.bot.send_message(keys.CHANNEL_ID, message,
                                         parse_mode=ParseMode.HTML
                                         )
                print("News Message send at: ", now,
                      file=open(C.LOG_FILE, 'a+'))
                time.sleep(1)
    return 0


def random_news(update: Update, context: CallbackContext) -> None:
    """Sends a random AWS news to user.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    news_index = random.randint(0, len(news_feed.entries))
    entry = news_feed.entries[news_index]
    message = message_creator(entry)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    print("Random News Message send at: ",
          datetime.now(), file=open(C.LOG_FILE, 'a+'))
