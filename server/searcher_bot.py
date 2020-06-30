import re
import time
import textwrap
from urllib.parse import quote_plus

import praw
from prawcore.exceptions import PrawcoreException
from praw.exceptions import RedditAPIException, ClientException
from praw.models import Comment, Message

from database import TaskerNetDatabase
from utils import *

reddit = praw.Reddit(PRAW_SITE_NAME)
db = TaskerNetDatabase()

REPLY_FOOTER = """
\n**Note**: Always check descriptions before importing anything. Never run anything unless you trust it completely.

---
^(Taskernet search powered by) ^[Algolia](https://www.algolia.com/).

^(I'm a bot made by /u/JustRollWithIt. See my source on) ^[Github](https://github.com/pghant/taskernet-collector)! 
"""

def search_reply(terms):
  results = db.search(terms)
  if len(results) == 0:
    return f'Sorry, I couldn\'t find any Taskernet links for "{terms}".' + REPLY_FOOTER
  reply = f'Hi, here\'s what I found for "{terms}":\n\n'
  for r in results:
    desc = remove_html_tags(r.description)
    desc = textwrap.shorten(desc, width=500, placeholder='...')
    reply += f'* [{r.name}]({r.url}) - {desc}\n'
    if len(r.source_links) > 0:
      reply += '  * '
      for link in r.source_links:
        reply += f'[[Source]({link})] '
      reply += '\n'
  results_link = f'https://pghant.github.io/taskernet-collector/search?q={quote_plus(terms)}'
  reply += f'\n**See more information and more results [here]({results_link}).**\n'
  reply += REPLY_FOOTER
  return reply

def process_comment(item):
  body = remove_unicode(item.body)
  if command := COLLECTOR_COMMAND_SEARCH_RE.search(body):
    replies = item.replies.list()
    if not any(m.author.name == 'taskernet-collector' for m in replies):
      item.reply(search_reply(command.group('terms')))

def process_message(item):
  body = remove_unicode(item.body)
  if command := COLLECTOR_COMMAND_SEARCH_RE.search(body):
    item.reply(search_reply(command.group('terms')))
    item.mark_read()

def main():
  running = True
  while running:
    try:
      for item in reddit.inbox.stream():
        if item.was_comment:
          time.sleep(30) # Wait to process in case there are edits
          try:
            item.refresh()
            item.replies.replace_more()
            process_comment(item)
          except ClientException as client_exception:
            print(f'Got client exception {client_exception}')
        else:
          process_message(item)
    except KeyboardInterrupt:
      print('Ending now')
      running = False
    except RedditAPIException as exception:
      time.sleep(300)
    except PrawcoreException:
      time.sleep(15)

if __name__ == '__main__':
  main()