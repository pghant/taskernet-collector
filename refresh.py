# Refresh shares

from database import TaskerNetDatabase

db = TaskerNetDatabase()

total_shares = db.record_count()

