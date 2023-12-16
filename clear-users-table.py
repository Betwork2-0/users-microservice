from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://betworkdev:betworkdev@cluster0.ktcz1j8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db
transactions = db.transactions

#delete all records in the users table
db.users.delete_many({})