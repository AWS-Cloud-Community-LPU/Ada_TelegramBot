"""
MIT License
Copyright (c) 2021 AWS Cloud Community LPU
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


import re
from datetime import datetime
from string import Template
import time
import random
from os import path
import feedparser
from telegram.ext import CallbackContext
from telegram import ParseMode, Update
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import constants as C


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


# Scope of Google Calendar API
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def fetch_events():
    """Fetches Event from google Calender.

    Returns:
    Events: JSON
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w', encoding='utf8') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now().astimezone().isoformat()

    # Call the Calendar API
    events_result = service.events().list(calendarId=C.CALENDAR_ID, timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    return events


def events_command(update: Update, context: CallbackContext):
    """Shows Upcoming events: Fetches events from fetch_events()

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    log_text = "Command: Events\n"
    log_text = log_text + f"Time: {get_time(update)}\n"
    username = get_username(update, context)
    log_text = log_text + f"User: {username}\n"
    print_logs(log_text)
    events = fetch_events()
    event_counter = 1
    # If list is empty
    if not events:
        update.message.reply_text("No upcoming events found.")
        return
    e_message = ""
    for event in events:
        start = event['start']['dateTime']
        start = start[:-6]
        end = event['end']['dateTime']
        end = end[:-6]
        start = datetime.strptime(
            start, '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p %d/%m/%Y')
        end = datetime.strptime(
            end, '%Y-%m-%dT%H:%M:%S').strftime('%I:%M %p %d/%m/%Y')
        summary = event['summary']
        try:
            description = event['description']
        except KeyError:
            description = "None"
        try:
            meet_link = event['hangoutLink']
        except KeyError:
            meet_link = "None"
        e_message = Template(C.EVENTS_TEMPLATE).substitute(
            eno=event_counter, start=start, end=end, summary=summary,
            description=description, meet_link=meet_link)
        event_counter = event_counter + 1
        update.message.reply_text(e_message, parse_mode=ParseMode.MARKDOWN)


def print_logs(log_message):
    """Writes logs in logs.txt
    """
    line = "-------------\n"
    log_message = line + log_message + line
    with open(C.LOG_FILE, 'a+', encoding='utf8') as log_file:
        print(log_message, file=log_file)


def check_status(update: Update, context: CallbackContext) -> int:
    """Checks status if brodcast news was sent from a specific username,
    and if brod_news command is only invoked once.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    log_text = "Command: Brodcast News\n"
    log_text = log_text + f"Time: {get_time(update)}\n"
    username = get_username(update, context)
    log_text = log_text + f"User: {username}\n"
    if username == "garvit_joshi9":  # Sent from Developer
        log_text = log_text + "Test Case #1: SUCCESS\n"
    else:
        log_text = log_text + "Test Case #1: FAILED\n"
        update.message.reply_text(C.ERROR_OWNER, parse_mode=ParseMode.MARKDOWN)
        print_logs(log_text)
        return -1
    if C.BRODCAST_NEWS_FLAG == 0:
        log_text = log_text + "Test Case #2: SUCCESS\n"
    else:
        log_text = log_text + "Test Case #2: FAILED\n"
        update.message.reply_text(
            C.ERROR_BRODCAST_AGAIN, parse_mode=ParseMode.MARKDOWN)
        print_logs(log_text)
        return -1
    C.BRODCAST_NEWS_FLAG = 1
    print_logs(log_text)
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
    if summary != "":
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
        if str(current_time) in ("13:00:00", "13:00:01", "13:00:02"):
            time.sleep(3)
            return "Afternoon"
        if str(current_time) in ("17:30:00", "17:30:01", "17:30:02"):
            time.sleep(3)
            return "Evening"
        if str(current_time) in ("21:00:00", "21:00:01", "21:00:02"):
            time.sleep(3)
            return "Night"


def feed_parser():
    """Parses feed of AWS What's new and gives non duplicate news.
    """
    if not path.exists(C.TITLE_STORE):
        with open(C.TITLE_STORE, 'a', encoding='utf-8'):
            pass
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    with open(C.TITLE_STORE, "r", encoding='utf-8') as title_file:
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
        with open(C.TITLE_STORE, 'a+', encoding='utf-8') as title_file:
            print(entry.title, file=title_file)
        message = message_creator(entry, time_status)
        context.bot.send_message(
            C.CHANNEL_ID, message, parse_mode=ParseMode.HTML)
        log_text = f"Brodcasted News send at: {get_time()}\n"
        print_logs(log_text)
        time.sleep(1)


def random_news(update: Update, context: CallbackContext) -> None:
    """Sends a random AWS news to user.

    Keyword arguments:
        update : This object represents an incoming update.
        context : This is a context object error handler.
    """
    news_feed = feedparser.parse(C.AWS_FEED_URL)
    news_index = random.randint(0, len(news_feed.entries)-1)
    entry = news_feed.entries[news_index]
    message = message_creator(entry)
    update.message.reply_text(message, parse_mode=ParseMode.HTML)
    log_text = "Command: Random news\n"
    log_text = log_text + f"Time: {get_time(update)}\n"
    log_text = log_text + f"User: {get_username(update, context)}\n"
    print_logs(log_text)
