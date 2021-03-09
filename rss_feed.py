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
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the group
    user_status = context.bot.getChatMember(chat_id, user_id).status
    #user_status contains ("creator", "administrator" or "member")
    if str(chat_id) == keys.CHANNEL_ID:
        print("Test Case #1: Success")
    else:
        print("Test Case #1: FAILED")
        print("Chat ID:", chat_id)
        update.message.reply_text(C.ERROR_CHAT_ID,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1
    if user_status == "creator":
        print("Test Case #2: Success")
    else:
        print("Test Case #2: FAILED")
        print("User ID:", user_id)
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
    """Brodcasts news after every certain time interval

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    brodcast_counter = 0
    if check_status(update, context) == -1:
        return -1
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    aws_file = "published_log.txt"
    aws_r_file = open(aws_file, "r")
    last_date = aws_r_file.readline()
    aws_r_file.close()

    for entry in reversed(news_feed.entries):
        published = entry.published
        date_time = datetime.strptime(published, '%a, %d %b %Y %H:%M:%S %z')
        date_time = str(date_time.date()) + " " + str(date_time.time())

        if date_time > last_date and brodcast_counter <= 4:
            message = message_creator(entry)
            context.bot.send_message(keys.CHANNEL_ID, message,
                                     parse_mode=ParseMode.HTML
                                     )
            brodcast_counter = brodcast_counter + 1
            print(date_time, file=open(aws_file, 'w'))
            last_date = date_time
            time.sleep(12 * 60 *60)  #12-Hours
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
    message = message_creator( entry )
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
