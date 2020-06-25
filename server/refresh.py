# Refresh shares

import time
import datetime as dt
import logging

from database import TaskerNetDatabase

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.WARNING, filename='refresh.log')

db = TaskerNetDatabase()

total_shares = db.record_count()

# shares to run every 30 minutes to cover all in one week
shares_to_run = total_shares // (24*6*2)
previous_week = int((dt.datetime.now() - dt.timedelta(days=7)).timestamp())

records_to_update = db.records_modified_before(previous_week, shares_to_run)

for record in records_to_update:
  try:
    db.update_share(record.id, record.url)
    time.sleep(3)
  except:
    logging.warning(f'Error when refreshing: {record.id}')
