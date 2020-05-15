# Backup Algolia database to JSON file

import json
import os

from algoliasearch.search_client import SearchClient

api_key = os.getenv('ALGOLIA_API_KEY')
app_id = os.getenv('ALGOLIA_APP_ID')

client = SearchClient.create(app_id, api_key)
share_index = client.init_index('shares')

hits = []

for hit in share_index.browse_objects({'query': ''}):
  hits.append(hit)

with open('backup.json', 'w') as f:
  json.dump(hits, f)