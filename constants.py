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

from threading import Semaphore


LOG_FILE = "Main.log"  # logs message and important data

TITLE_FILE = "titles.txt"  # logs titles of news that are already sent(DEFAULT)

DEVELOPERS = []  # Usernames of developers(Will be loded from config)

BRODCAST_NEWS_FLAG = Semaphore()  # Only one instance of Brodcast news should be running

CALENDAR_ID = "GOOGLE CALENDER ID"  # Will be loded from config

CHANNEL_ID = "TELEGRAM CHANNEL ID"  # Will be loded from config

AWS_FEED_URL = "https://aws.amazon.com/about-aws/whats-new/recent/feed/"

BRODCAST_NEWS = "News will be periodically sent at 9:00am, 1:00pm, 5:30pm and 9:00pm\n"

HELP_TEXT = """
Hey There!
My name is Ada. I was made in loving memory of Ada Lovelace, The First Computer Programmer.
Currently, I am in Development. Some commands that I support:
1. /start
2. /help
3. /events
4. /source
5. /news
6. /brod_news : Currently supported for owners of this group.

As I am an Open Source Project, You can contribute to my development.
Link: http://bit.ly/AdaSource
I am learning new things everyday. \U0001F609
"""

SOURCE = """
Hey there $name,
You can find my Source code at http://bit.ly/AdaSource
In case of bottlenecks please feel free to message @garvit_joshi9.
Happy Coding !! \U0001F60E
"""

NO_EVENTS = """
Currently, No events are scheduled.
"""

ERROR_OWNER = """
Sorry, The command can only be executed by owners.
"""

ERROR_BRODCAST_AGAIN = """News are already being sent.\n"""

EVENTS_TEMPLATE = """
**Event No.:** $eno
**Start Time:** $start
**End Time:** $end
**Summary:** $summary
**Description:** $description
**Meet Link:** $meet_link
"""
