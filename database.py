import os

import requests
from algoliasearch.search_client import SearchClient
from urllib.parse import urlparse, parse_qs, quote_plus

class SearchResult():
  def __init__(self, result):
    self.name = result['name']
    self.url = result['url']
    self.description = result['description']


class TaskerNetDatabase():
  def __init__(self):
    api_key = os.getenv('ALGOLIA_API_KEY')
    app_id = os.getenv('ALGOLIA_APP_ID')
    self.db = SearchClient.create(app_id, api_key)
    self.shares_index = self.db.init_index('shares')
  
  def add_share(self, share_link):
    parsed = urlparse(share_link)
    qparams = parse_qs(parsed.query)

    user = quote_plus(qparams['user'][0])
    share_id = quote_plus(qparams['id'][0])

    resp = requests.get(f'https://taskernet.com/_ah/api/datashare/v1/shares/{user}/{share_id}')

    if resp.status_code != 200:
      return False

    share_data = resp.json()

    date = None
    try:
      date = int(share_data['info']['date'])
    except ValueError:
      pass

    self.shares_index.save_object({
      'objectID': f'{user}_{share_id}',
      'type': share_data['info']['type'],
      'name': share_data['info']['name'],
      'description': share_data['info']['description'],
      'date': date,
      'views': share_data['info']['stats']['views'],
      'downloads': share_data['info']['stats']['downloads'],
      'url': share_data['info']['url']
    })

    return True

  def search(self, query):
    request_options = {
      'hitsPerPage': 5,
      'attributesToRetrieve': ['name', 'url', 'description'],
      'attributesToHighlight': []
    }
    res = self.shares_index.search(query, request_options)
    return [SearchResult(r) for r in res['hits']]
