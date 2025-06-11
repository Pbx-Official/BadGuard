import config
import pytz

from Bad.core.bot import jass, Bad, application
from Bad.core.dir import dirr
from Bad.core.git import git
from Bad.misc import dbb, heroku
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .logging import LOGGER


dirr()
git()
dbb()
heroku()

app = jass()
Bad = Bad()
application = application

HELPABLE = {}

#TIME ZONE 
TIME_ZONE = pytz.timezone(config.TIME_ZONE)
scheduler = AsyncIOScheduler(timezone=TIME_ZONE)
