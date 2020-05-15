import re

PRAW_SITE_NAME = 'taskernet_bot'
MONITORED_SUBREDDITS = 'tasker+taskernet+justrollwithittest'

TASKERNET_RE = re.compile(r'https://taskernet\.com/shares.*?id=[\w\d+%]+')
COLLECTOR_COMMAND_SEARCH_RE = re.compile(r'/?u/taskernet-collector search "(?P<terms>.*?)"', re.IGNORECASE)
COLLECTOR_COMMAND_PM_SEARCH_RE = re.compile(r'search "(?P<terms>.*?)"', re.IGNORECASE)
HTML_TAG_RE = re.compile(r'<.*?>')
UNICODE_RE = re.compile(r'[^\x00-\x7F]+')

def remove_html_tags(text):
  return re.sub(HTML_TAG_RE, '', text)

def remove_unicode(text):
  return re.sub(UNICODE_RE, ' ', text)