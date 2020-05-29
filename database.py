import os
import time
import logging

import requests
from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import RequestException

from utils import COLLECTOR_IGNORE_RE, share_object_id, parse_link

class SearchResult():
  def __init__(self, result):
    self.name = result['name']
    self.url = result['url']
    self.description = result['description']
    self.source_links = result['sourceLinks'] if 'sourceLinks' in result else []


class TaskerNetDatabase():
  def __init__(self):
    api_key = os.getenv('ALGOLIA_API_KEY')
    app_id = os.getenv('ALGOLIA_APP_ID')
    self.db = SearchClient.create(app_id, api_key)
    self.shares_index = self.db.init_index('shares')
  
  def get_share_by_id(self, object_id):
    try:
      return self.shares_index.get_object(object_id)
    except RequestException:
      return None
  
  def add_share(self, share_link, source_link):
    user, share_id = parse_link(share_link)
    object_id = share_object_id(user=user, share_id=share_id)
    if object_id == None:
      logging.warning(f'Invalid share link: {share_link} at {source_link}')
      return False
    existing_object = self.get_share_by_id(object_id)

    resp = requests.get(f'https://taskernet.com/_ah/api/datashare/v1/shares/{user}/{share_id}')

    # Share link is removed. Delete any stored record
    if resp.status_code == 404:
      if existing_object != None:
        self.shares_index.delete_object(object_id)
      return True
    elif resp.status_code != 200: # some other error
      logging.warning(f'Error when adding: {share_link}, {source_link}')
      return False

    # Check if the share description has a tag to ignore this share. Delete any stored record
    share_data = resp.json()
    if COLLECTOR_IGNORE_RE.search(share_data['info']['description']):
      if existing_object != None:
        self.shares_index.delete_object(object_id)
      return False

    # Add this source link to existing source links if any
    source_links = [source_link]
    if existing_object != None and 'sourceLinks' in existing_object:
      source_links.extend(existing_object['sourceLinks'])
      source_links = list(set(source_links))

    date = None
    try:
      date = int(share_data['info']['date'])
    except ValueError:
      pass

    self.shares_index.save_object({
      'objectID': object_id,
      'sourceLinks': source_links,
      'type': share_data['info']['type'],
      'name': share_data['info']['name'],
      'description': share_data['info']['description'],
      'date': date,
      'views': share_data['info']['stats']['views'],
      'downloads': share_data['info']['stats']['downloads'],
      'url': share_data['info']['url'],
      'recordUpdated': int(time.time())
    })

    return True

  def search(self, query):
    request_options = {
      'hitsPerPage': 5,
      'attributesToRetrieve': ['name', 'url', 'description', 'sourceLinks'],
      'attributesToHighlight': []
    }
    res = self.shares_index.search(query, request_options)
    return [SearchResult(r) for r in res['hits']]
  
  def record_count(self):
    request_options = {
      'hitsPerPage': 0,
      'attributesToRetrieve': [],
      'attributesToHighlight': []
    }
    res = self.shares_index.search('', request_options)
    return res['nbHits']
