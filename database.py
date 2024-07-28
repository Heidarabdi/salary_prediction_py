from tinydb import TinyDB, Query

db = TinyDB('db.json')
user_table = db.table('user')
prediction_table = db.table('prediction')

Query = Query()
