# Use PushshiftAPI to get historic taskernet links
# Goes through comments and submissions from past 8 days and adds if not already existing

import re
import time
from itertools import chain
import logging
import datetime as dt

import praw
from psaw import PushshiftAPI

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, share_object_id

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING, filename='historic.log')

reddit = praw.Reddit(PRAW_SITE_NAME)
api = PushshiftAPI(reddit)
db = TaskerNetDatabase()

subs_to_search = ['tasker', 'taskernet']
start_epoch = int((dt.datetime.now() - dt.timedelta(days=8)).timestamp())

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
      # Add share if it doesn't exist already
      object_id = share_object_id(share_link=link)
      if object_id != None and db.get_share_by_id(object_id) == None:
        success = db.add_share(link, source_link)
        time.sleep(10) # don't overload API
      else:
        success = True
    except:
      logging.warning(f'Add share exception: {source_link}')
      success = False
    if not success:
      logging.warning(f'Add share failed: {source_link}')

def process_comments(comments):
  logging.info(f'Starting comments')
  completed = 0
  for comment in comments:
    taskernet_links = TASKERNET_RE.findall(comment.body)
    if comment.author != None and comment.author.name != 'taskernet-collector' and len(taskernet_links) > 0:
      source_link = f'https://reddit.com/comments/{comment.link_id[3:]}/_/{comment.id}'
      add_shares(taskernet_links, source_link)
      completed += 1
      if completed % 10 == 0:
        logging.info(f'Completed: {completed}')
  logging.info(f'Finished comments: {completed}')

def process_submissions(submissions):
  logging.info(f'Starting submissions')
  completed = 0
  for submission in submissions:
    taskernet_links = TASKERNET_RE.findall(f'{submission.url} {submission.selftext}')
    if len(taskernet_links) > 0:
      source_link = f'https://redd.it/{submission.id}'
      add_shares(taskernet_links, source_link)
      completed += 1
      if completed % 10 == 0:
        logging.info(f'Completed: {completed}')
  logging.info(f'Finished submissions: {completed}')

def main():
  all_comments = get_comments()
  all_posts = get_posts()
  process_comments(all_comments)
  process_submissions(all_posts)

if __name__ == '__main__':
  main()