from event_finder import db_updates 
from webinarguru.settings import DEBUG

print("debug:", DEBUG)
db_updates.load_dummy_events_to_db()