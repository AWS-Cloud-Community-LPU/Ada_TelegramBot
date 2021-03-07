import re
from datetime import datetime
import time
import secrets as keys
import constants as C
import feedparser
from telegram.ext import CallbackContext
from telegram import ParseMode, Update


def check_status(update, context) -> int:
    chat_id = update.message.chat_id    #Channel ID of the group
    user_id = update.message.from_user.id    #User ID of the group
    user_status = context.bot.getChatMember(chat_id, user_id).status
    print(user_status)
    #user_status = contains ("creator", "administrator" or "member")
    if str(chat_id) == keys.CHANNEL_ID:
        print("Test Case #1: Success")
    else:
        print("Test Case #1: FAILED")
        print("Chat ID:", chat_id)
        update.message.reply_text("Sorry, The command can only be executed in [this](t.me/awscclpu) Group",
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1
    if user_status == "creator":
        print("Test Case #2: Success")
    else:
        print("Test Case #1: FAILED")
        print("User ID:", user_id)
        update.message.reply_text("Sorry, The command can only be executed by [owner](t.me/garvit_joshi9)",
                                  parse_mode=ParseMode.MARKDOWN
                                  )
        return -1


def brodcast_news(update: Update, context: CallbackContext):
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
        
        if date_time > last_date:
            title = "<b>Title: " + entry.title + "</b>"
            cleanr = re.compile(
                '<.*?>|&([a-z0-9]+|#[0-9]{1,6}|#x[0-9a-f]{1,6});')
            summary = re.sub(cleanr, '', entry.summary)
            summary = "\n\n<b>Summary:</b> " + summary
            link = "\n\n<b>Link: </b>" + "<a href=\"" + entry.link + "\">Click here</a>"
            message = title + summary + link
            context.bot.send_message(keys.CHANNEL_ID, message,
                                     parse_mode=ParseMode.HTML
                                     )
            print(date_time, file=open(aws_file, 'w'))
            last_date = date_time
            time.sleep(60)
    return 0
