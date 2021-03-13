import re
from datetime import datetime
import time
import secrets as keys
import random
from os import path
import feedparser
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
import constants as C


def check_status(update: Update, context: CallbackContext) -> int:
    """Checks status if brodcast news was sent from a specific username.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    print(f"Brodcast News at: {datetime.now()}", file=open(
        C.LOG_FILE, 'a+'))
    chat_id = update.message.chat_id  # Channel ID of the group
    user_id = update.message.from_user.id  # User ID of the person
    username = context.bot.getChatMember(chat_id, user_id).user.username
    if username == "garvit_joshi9":  # Sent from Developer
        print("Test Case #1: Success", file=open(C.LOG_FILE, 'a+'))
    else:
        print("Test Case #1: FAILED\nUserName:",
              username, file=open(C.LOG_FILE, 'a+'))
        update.message.reply_text(C.ERROR_OWNER,
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1
    return 0


def message_creator(entry, greetings="None") -> str:
    """Returns news in a proper format

    Keyword arguments:
        entry : a perticular entry of rss feed used for extracting data.
        greetings : "None" in case of random news and function defined
    """
    title = "<b>Title: " + entry.title + "</b>"
    cleanr = re.compile(
        '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
    summary = re.sub(cleanr, '', entry.summary)
    summary = "\n\n<b>Summary:</b> " + summary
    link = "\n\n<b>Link: </b>" + "<a href=\"" + entry.link + "\">Click here</a>"
    message = title + summary + link
    if greetings == "morning":
        message = "<b> Good Morning Everyone </b>\n\n" + message
    elif greetings == "night":
        message = message + "\n\n<b> Good Night Everyone </b>"
    return message


def check_time() -> str:
    """
    Checks time

    Return:
        "morning" : if time is 9AM.
        "night" " if time is 9PM.
    """
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(1)
        if str(current_time) in ("09:00:00", "09:00:01", "09:00:02"):
            time.sleep(1)
            return "morning"
        if str(current_time) in ("21:00:00", "21:00:01", "21:00:02"):
            time.sleep(1)
            return "night"


def feed_parser():
    """Parses feed of AWS What's new and gives non duplicate news.
    """
    if not path.exists(C.TITLE_STORE):
        open(C.TITLE_STORE, 'a').close()
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    with open(C.TITLE_STORE, "r") as title_file:
        line_titles = title_file.readlines()
        for entry in news_feed.entries:
            flag = 0
            for line_title in line_titles:
                if str(entry.title)+"\n" == line_title:
                    flag = 1
            if flag == 0:
                return entry
    return news_feed.entries[0]


def brodcast_news(update: Update, context: CallbackContext):
    """Brodcasts news at 9:00am and 9:00pm everyday.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    if check_status(update, context) == -1:
        return -1
    update.message.reply_text("News will be periodically sent at 9:00am and 9:00pm",
                              parse_mode=ParseMode.MARKDOWN
                              )
    while True:
        entry = feed_parser()
        time_status = check_time()
        if time_status == "morning":
            print(entry.title, file=open(C.TITLE_STORE, 'a+'))
            message = message_creator(entry, "morning")
            context.bot.send_message(keys.CHANNEL_ID, message,
                                     parse_mode=ParseMode.HTML
                                     )
            print("Brodcasted News send at: ", datetime.now(),
                  file=open(C.LOG_FILE, 'a+'))
            time.sleep(1)
        if time_status == "night":
            print(entry.title, file=open(C.TITLE_STORE, 'a+'))
            message = message_creator(entry, "night")
            context.bot.send_message(keys.CHANNEL_ID, message,
                                     parse_mode=ParseMode.HTML
                                     )
            print("Brodcasted News send at: ", datetime.now(),
                  file=open(C.LOG_FILE, 'a+'))
            time.sleep(1)


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
