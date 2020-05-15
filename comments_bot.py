import re
import time

import praw
from prawcore.exceptions import PrawcoreException

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, MONITORED_SUBREDDITS

reddit = praw.Reddit(PRAW_SITE_NAME)
subreddit = reddit.subreddit(MONITORED_SUBREDDITS)

db = TaskerNetDatabase()

running = True
while running:
  try:
    for comment in subreddit.stream.comments():
      if comment.author.name != 'taskernet-collector':
        taskernet_links = TASKERNET_RE.findall(comment.body)
        for link in taskernet_links:
          db.add_share(link)
  except KeyboardInterrupt:
    print('Ending now')
    running = False
  except PrawcoreException:
    time.sleep(15)
