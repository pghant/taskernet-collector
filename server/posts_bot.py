import re
import time
import logging

import praw
from prawcore.exceptions import PrawcoreException

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, MONITORED_SUBREDDITS

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING, filename='posts_bot.log')

reddit = praw.Reddit(PRAW_SITE_NAME)
subreddit = reddit.subreddit(MONITORED_SUBREDDITS)

db = TaskerNetDatabase()

running = True
while running:
  try:
    for submission in subreddit.stream.submissions():
      source_link = f'https://redd.it/{submission.id}'
      taskernet_links = TASKERNET_RE.findall(f'{submission.url} {submission.selftext}')
      for link in taskernet_links:
        db.add_share(link, source_link)
  except KeyboardInterrupt:
    print('Ending now')
    running = False
  except PrawcoreException:
    time.sleep(15)
