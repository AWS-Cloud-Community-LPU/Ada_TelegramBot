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
import main as M


def check_status(update: Update, context: CallbackContext) -> int:
    """Checks status if brodcast news was sent from a specific username,
    and if brod_news command is only invoked once.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    log_text = "Command: Brodcast News\n"
    log_text = log_text + f"Time: {M.get_time()}\n"
    username = M.get_username(update, context)
    log_text = log_text + f"User: {username}\n"
    if username == "garvit_joshi9":  # Sent from Developer
        log_text = log_text + "Test Case #1: SUCCESS\n"
    else:
        log_text = log_text + "Test Case #1: FAILED\n"
        update.message.reply_text(C.ERROR_OWNER, parse_mode=ParseMode.MARKDOWN)
        M.print_logs(log_text)
        return -1
    if C.BRODCAST_NEWS_FLAG == 0:
        log_text = log_text + "Test Case #2: SUCCESS\n"
    else:
        log_text = log_text + "Test Case #2: FAILED\n"
        update.message.reply_text(
            C.ERROR_BRODCAST_AGAIN, parse_mode=ParseMode.MARKDOWN)
        M.print_logs(log_text)
        return -1
    C.BRODCAST_NEWS_FLAG = 1
    M.print_logs(log_text)
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
    if greetings in ("Morning", "Afternoon", "Evening"):
        message = "<b> Good " + greetings + " Everyone </b>\n\n" + message
    elif greetings == "Night":
        message = message + "\n\n<b> Good " + greetings + " Everyone </b>"
    return message


def check_time() -> str:
    """
    Checks time

    Return:
        "Morning" : if time is 9AM.
        "Afternoon" : if time is 1PM.
        "Evening" : if time is 5:30PM.
        "Night" : if time is 9PM.
    """
    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        time.sleep(1)
        if str(current_time) in ("09:00:00", "09:00:01", "09:00:02"):
            time.sleep(3)
            return "Morning"
        elif str(current_time) in ("13:00:00", "13:00:01", "13:00:02"):
            time.sleep(3)
            return "Afternoon"
        elif str(current_time) in ("17:30:00", "17:30:01", "17:30:02"):
            time.sleep(3)
            return "Evening"
        elif str(current_time) in ("21:00:00", "21:00:01", "21:00:02"):
            time.sleep(3)
            return "Night"


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
    """Brodcasts news at 9:00am, 1:00pm, 5:30pm and 9:00pm everyday.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    if check_status(update, context) == -1:
        return -1
    update.message.reply_text(C.BRODCAST_NEWS, parse_mode=ParseMode.MARKDOWN)
    while True:
        entry = feed_parser()
        time_status = check_time()
        print(entry.title, file=open(C.TITLE_STORE, 'a+'))
        message = message_creator(entry, time_status)
        context.bot.send_message(
            keys.CHANNEL_ID, message, parse_mode=ParseMode.HTML)
        log_text = f"Brodcasted News send at: {M.get_time()}\n"
        M.print_logs(log_text)
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
    log_text = "Command: Random news\n"
    log_text = log_text + f"Time: {M.get_time(update)}\n"
    log_text = log_text + f"User: {M.get_username(update, context)}\n"
    M.print_logs(log_text)
