from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
uri = "mongodb+srv://betworkdev:betworkdev@cluster0.ktcz1j8.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client.db
transactions = db.transactions
print(transactions.find_one({}))
print("Connected to MongoDB")

# Print all the tables that exist in the db
print(db.list_collection_names())

#delete all users with the name of game
db.users.delete_many({'name': 'game'})


# Print out all the records from the 'users' table
for record in db.users.find({}):
    print(record)


# return all users with the name 'Sam' from the 'users' table
for record in db.users.find({'name': 'not a user'}):
    print(record)

# Check if a user named game exists in the 'users' table, if not, create one 
if db.users.find_one({'name': 'game'}) is None:
    db.users.insert_one({'name': 'game', 'age': 30, 'occupation': 'Software Engineer'})

# insert a new record into the 'users' table
test = db.users.insert_one({'user_name': 'Samwell', 'age': 30, 'occupation': 'Software Engineer'})

# print out all the records
for record in db.users.find({}):
    print(record)

# add a friends array to the users table and add a new user with username 'friendly' and friends 'super', 'duper', 'friendly'
db.users.insert_one({'user_name': 'friendly', 'email':'123@dang.com', 'age': 30, 'friends': ['super', 'duper', 'friendly']})

