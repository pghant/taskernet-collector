import re
from urllib.parse import urlparse, parse_qs, quote_plus

PRAW_SITE_NAME = 'taskernet_bot'
MONITORED_SUBREDDITS = 'tasker+taskernet'

TASKERNET_RE = re.compile(r'https://taskernet\.com/shares[^\\]*?id=[\w\d+%.-]+')
COLLECTOR_COMMAND_SEARCH_RE = re.compile(r'search "(?P<terms>.*?)"', re.IGNORECASE)
HTML_TAG_RE = re.compile(r'<.*?>')
UNICODE_RE = re.compile(r'[^\x00-\x7F]+')
COLLECTOR_IGNORE_RE = re.compile(r'\[no\-collect\]')

def remove_html_tags(text):
  return re.sub(HTML_TAG_RE, '', text)

def remove_unicode(text):
  return re.sub(UNICODE_RE, ' ', text)

# Either share_link or both user and share_id are required
def share_object_id(share_link=None, user=None, share_id=None):
  try:
    if share_link != None:
      user, share_id = parse_link(share_link)
    return f'{user}_{share_id}'
  except:
    return None

def parse_link(share_link):
  try:
    parsed = urlparse(share_link)
    qparams = parse_qs(parsed.query)

    user = quote_plus(qparams['user'][0])
    share_id = quote_plus(qparams['id'][0])
    return user, share_id
  except:
    return None, None
