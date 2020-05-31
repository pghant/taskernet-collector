# Backup Algolia database to JSON file

import json
import os

from algoliasearch.search_client import SearchClient

api_key = os.getenv('ALGOLIA_API_KEY')
app_id = os.getenv('ALGOLIA_APP_ID')

client = SearchClient.create(app_id, api_key)
share_index = client.init_index('shares')
plugin_index = client.init_index('plugins')

def backup_index(index):
  hits = []

  for hit in index.browse_objects({'query': ''}):
    hits.append(hit)

  with open(f'backup-{index}.json', 'w') as f:
    json.dump(hits, f)

backup_index(share_index)
backup_index(plugin_index)