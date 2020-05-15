# Use PushshiftAPI to get historic taskernet links

import re
import time

import praw
from psaw import PushshiftAPI

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, MONITORED_SUBREDDITS

reddit = praw.Reddit(PRAW_SITE_NAME)
api = PushshiftAPI(reddit)
db = TaskerNetDatabase()

subs_to_search = MONITORED_SUBREDDITS.replace('+', ',')

all_comments = api.search_comments(q='taskernet', subreddit=subs_to_search)
all_posts = api.search_submissions(q='taskernet', subreddit=subs_to_search)

print('Starting comments')
completed = 0

for comment in all_comments:
  taskernet_links = TASKERNET_RE.findall(comment.body)
  for link in taskernet_links:
    db.add_share(link)
    completed += 1
    if completed % 10 == 0:
      print(f'Completed: {completed}')
    time.sleep(1) # don't overload API

print(f'Finished comments: {completed}')
print('Starting posts')
completed = 0

for submission in all_posts:
  taskernet_links = TASKERNET_RE.findall(f'{submission.url} {submission.selftext}')
  for link in taskernet_links:
    db.add_share(link)
    completed += 1
    if completed % 10 == 0:
      print(f'Completed: {completed}')
    time.sleep(1) # don't overload API

print(f'Finished posts: {completed}')
