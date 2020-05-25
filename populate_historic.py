# Use PushshiftAPI to get historic taskernet links
# Goes through all historic reddit submissions and comments since Taskernet was introduced
# Will take a long time to process everything

import re
import time
from itertools import chain
import logging
import datetime as dt

import praw
from psaw import PushshiftAPI

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, MONITORED_SUBREDDITS

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING, filename='historic.log')

reddit = praw.Reddit(PRAW_SITE_NAME)
api = PushshiftAPI(reddit)
db = TaskerNetDatabase()

subs_to_search = ['tasker', 'taskernet']
start_epoch = int(dt.datetime(2018, 9, 18).timestamp())

def get_comments():
  gens = []
  for sub in subs_to_search:
    gens.append(api.search_comments(after=start_epoch, subreddit=sub))
  return chain(*gens)

def get_posts():
  gens = []
  for sub in subs_to_search:
    gens.append(api.search_submissions(after=start_epoch, subreddit=sub))
  return chain(*gens)

def add_shares(taskernet_links, source_link):
  for link in taskernet_links:
    try:
      success = db.add_share(link, source_link)
    except:
      logging.warning(f'Add share exception: {source_link}')
      success = False
    if not success:
      print(f'Add share failed: {source_link}')
      logging.warning(f'Add share failed: {source_link}')
    time.sleep(10) # don't overload API

def main():
  all_comments = get_comments()
  all_posts = get_posts()

  print('Starting comments')
  completed = 0

  for comment in all_comments:
    taskernet_links = TASKERNET_RE.findall(comment.body)
    if comment.author != None and comment.author.name != 'taskernet-collector' and len(taskernet_links) > 0:
      source_link = f'https://reddit.com/comments/{comment.link_id[3:]}/_/{comment.id}'
      add_shares(taskernet_links, source_link)
      completed += 1
      if completed % 10 == 0:
        print(f'Completed: {completed}')

  print(f'Finished comments: {completed}')
  print('Starting posts')
  completed = 0

  for submission in all_posts:
    taskernet_links = TASKERNET_RE.findall(f'{submission.url} {submission.selftext}')
    if len(taskernet_links) > 0:
      source_link = f'https://redd.it/{submission.id}'
      add_shares(taskernet_links, source_link)
      completed += 1
      if completed % 10 == 0:
        print(f'Completed: {completed}')

  print(f'Finished posts: {completed}')

if __name__ == '__main__':
  main()