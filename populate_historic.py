# Use PushshiftAPI to get historic taskernet links

import re
import time
from itertools import chain

import praw
from psaw import PushshiftAPI

from database import TaskerNetDatabase
from utils import TASKERNET_RE, PRAW_SITE_NAME, MONITORED_SUBREDDITS

reddit = praw.Reddit(PRAW_SITE_NAME)
api = PushshiftAPI(reddit)
db = TaskerNetDatabase()

subs_to_search = ['tasker', 'taskernet']

def get_comments():
  gens = []
  for sub in subs_to_search:
    gens.append(api.search_comments(q='taskernet', subreddit=sub))
  return chain(*gens)

def get_posts():
  gens = []
  for sub in subs_to_search:
    gens.append(api.search_submissions(q='taskernet', subreddit=sub))
  return chain(*gens)

def add_shares(taskernet_links, source_link):
  for link in taskernet_links:
    db.add_share(link, source_link)
    time.sleep(1) # don't overload API

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