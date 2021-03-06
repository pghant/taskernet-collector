import os
import time
import logging

import requests
from algoliasearch.search_client import SearchClient
from algoliasearch.exceptions import RequestException

import utils
import taskernet_api as api
import googleplay_api as gplay

class SearchResult():
  def __init__(self, result):
    self.id = result['objectID'] if 'objectID' in result else None
    self.name = result['name'] if 'name' in result else None
    self.url = result['url'] if 'url' in result else None
    self.description = result['description'] if 'description' in result else None
    self.source_links = result['sourceLinks'] if 'sourceLinks' in result else []

class TaskerNetDatabase():
  def __init__(self):
    api_key = os.getenv('ALGOLIA_API_KEY')
    app_id = os.getenv('ALGOLIA_APP_ID')
    self.db = SearchClient.create(app_id, api_key)
    self.shares_index = self.db.init_index('shares')
    self.shares_by_updated_index = self.db.init_index('shares_by_updated')
    self.plugins_index = self.db.init_index('plugins')
  
  def add_plugin(self, package):
    try:
      app_name = gplay.get_app_name(package)
      plugin = {
        'objectID': package,
        'appName': app_name,
      }
      self.plugins_index.save_object(plugin)
      return plugin
    except:
      logging.error(f'Error when adding plugin to index: {package}')
      return None
  
  def get_plugin(self, package):
    try:
      return self.plugins_index.get_object(package)
    except RequestException:
      return self.add_plugin(package)
  
  def get_share_by_id(self, object_id):
    try:
      return self.shares_index.get_object(object_id)
    except RequestException:
      return None
  
  def add_share(self, share_link, source_link):
    user, share_id = utils.parse_link(share_link)
    object_id = utils.share_object_id(user=user, share_id=share_id)
    if object_id is None:
      logging.warning(f'Invalid share link: {share_link} at {source_link}')
      return False
    existing_object = self.get_share_by_id(object_id)

    try:
      share_data = api.get_share_data(share_link)
      tasker_data = api.get_tasker_data(share_link)
    except api.ShareDoesNotExistError:
      # Share link is removed. Delete any stored record
      if existing_object is not None:
        self.shares_index.delete_object(object_id)
      return True
    except api.GenericError:
      logging.warning(f'Error when adding: {share_link}, {source_link}')
      return False

    # Check if the share description has a tag to ignore this share. Delete any stored record
    if utils.COLLECTOR_IGNORE_RE.search(share_data['info']['description']):
      if existing_object is not None:
        self.shares_index.delete_object(object_id)
      return True

    # Add this source link to existing source links if any
    source_links = [source_link]
    if existing_object is not None and 'sourceLinks' in existing_object:
      source_links.extend(existing_object['sourceLinks'])
      source_links = list(set(source_links))

    try:
      tags, names, plugin_packages = utils.parse_tasker_data(tasker_data)
    except:
      logging.warning(f'Error when parsing tasker data: {share_link}')
      return False
    
    for package in plugin_packages:
      if plugin := self.get_plugin(package):
        tags.append(plugin['appName'])

    date = None
    try:
      date = int(share_data['info']['date'])
    except ValueError:
      pass

    try:
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
        'recordUpdated': int(time.time()),
        'tags': tags,
        'names': names,
        'plugins': plugin_packages
      })
    except:
      logging.error(f'Error when adding to index: {share_link}')
      return False

    return True
  
  def update_share(self, object_id, share_link):
    try:
      share_data = api.get_share_data(share_link)
      tasker_data = api.get_tasker_data(share_link)
    except api.ShareDoesNotExistError:
      # Share link is removed. Delete record
      self.shares_index.delete_object(object_id)
      return True
    except api.GenericError:
      logging.warning(f'Error when updating: {share_link}')
      return False
    
    try:
      tags, names, plugin_packages = utils.parse_tasker_data(tasker_data)
    except:
      logging.warning(f'Error when parsing tasker data: {share_link}')
      return False
    
    for package in plugin_packages:
      if plugin := self.get_plugin(package):
        tags.append(plugin['appName'])

    date = None
    try:
      date = int(share_data['info']['date'])
    except ValueError:
      pass

    self.shares_index.partial_update_object({
      'objectID': object_id,
      'description': share_data['info']['description'],
      'date': date,
      'views': share_data['info']['stats']['views'],
      'downloads': share_data['info']['stats']['downloads'],
      'recordUpdated': int(time.time()),
      'tags': tags,
      'names': names,
      'plugins': plugin_packages
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
  
  def records_modified_before(self, timestamp, num_retrieve):
    request_options = {
      'attributesToRetrieve': ['url'],
      'attributesToHighlight': [],
      'filters': f'recordUpdated <= {timestamp}',
      'hitsPerPage': num_retrieve
    }
    res = self.shares_by_updated_index.search('', request_options)
    return [SearchResult(r) for r in res['hits']]
