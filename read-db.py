from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://betworkdev:betworkdev@cluster0.ktcz1j8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db
transactions = db.transactions
print(transactions.find_one({}))
print("Connected to MongoDB")

# print all records in the users table
for record in db.users.find({}):
    print(record)
    