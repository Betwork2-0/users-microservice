# getters
import os
from typing import Optional, Any
from fastapi import status, Response
import pymysql
from pydantic import BaseModel
from passlib.hash import bcrypt
import uuid
from email_verf import send_email
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


database_name = "users_db.users"
# database_name = "user_test.users"  # for local testing


class VerificationCode(BaseModel):
    verification_code: str


class Books(BaseModel):
    books: str


class UserSoftDelete(BaseModel):
    disable: bool

class Friends(BaseModel):
    user_name: str
    friend_user_name: str


class User(BaseModel):
    """
        User class model
    """
    user_name: str
    password: str
    solidity_address: Optional[str] = None
    email: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    google_id: Optional[str] = None
    liked_books: Optional[str] = None
    disable: bool = False
    verification_code: str = ""

    def verify_password(self, _password):
        return bcrypt.verify(_password, self.password)


class DbUsersSystem:
    """ This class is a helper class to connect to the system DB """
    def __int__(self):
        pass

    @staticmethod
    def get_connection():  # TODO: Change later localhost..
        #user = "admin"
        #password = "the_warriors"
        host = "mongodb+srv://betworkdev:betworkdev@cluster0.ktcz1j8.mongodb.net/?retryWrites=true&w=majority"
        # testing info
        # user = "root"
        # password = "Revamped1!"
        # host = "localhost"
        try:
            print("test 1")
            client = MongoClient(host, server_api=ServerApi('1'))
            print("test 2")
        except Exception:
            return None
        return client 

def get_all_friends(username: str):
    """
    returns all friends of a user
    """
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        result = db.users.find_one({'user_name': username})
        print(result)
        #if result has a friends field
        if result:
            friends = result.get('friends', [])
            ans = []
            print("DSFSDFDSF" + friends[0])
            if friends:
                print("LKSDJLKSDFLKJSDLKJSDLKJSDFJLK")
                for friend in friends:
                    print ("sdjlfalskdjf")
                    ans.append((friend, get_solidity_address(friend)))
                print("still ok")
                return {
                    "success": True,
                    "payload": ans
                }
            return {"success": False, "payload": "User has no friends"}
        return {"success": False, "payload": "User not found"}
    except Exception as e:
        return {"success": False, "payload": e}

def get_solidity_address(username: str):
    """
    returns the solidity address of a user
    """
    print("got here")
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        result = db.users.find_one({'user_name': username})
        if result:
            print(result['solidity_address'])
            return result['solidity_address']
        return "addr_err"
    except Exception as e:
        return "addr_err"

def get_user_by_solidity_address(solidity_address: str):
    """
    returns a user based on solidity address
    """
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        result = db.users.find_one({'solidity_address': solidity_address})
        print(result)
        if result:
            result['_id'] = str(result['_id'])
            return {
                "success": True,
                "payload": result
            }
        return {"success": False, "payload": "User Not Found"}
    except Exception as e:
        return {"success": False, "payload": e}


def search_friend(username: str):
    """
    returns a friend based on username
    """
    try:
        result = get_user_by_username(username) 
        print("Got Here in search_friend")
        print(result)
        if result:
            result['_id'] = str(result['_id'])
            return {
                "success": True,
                "payload": result
            }
        return {"success": False, "payload": "User Not Found"}
    except Exception as e:
        return {"success": False, "payload": e}


def execute_query(sql: str, argument: Optional[Any] = None):
    """
    This function takes sql query and returns its result
    :param sql: the sql statement
    :param argument: the needed argument
    :return: data
    """
    try:
        connection = DbUsersSystem.get_connection()
        if not connection:
            return Response(status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                            content="DB service is unavailable")
        cursor = connection.cursor()
        _ = cursor.execute(sql, args=argument)  # provide the number of results
        final_result = cursor.fetchall()  # provide the actual results (with data)
        return final_result
    except Exception:
        return None

def login(username:str, password:str):
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        result = db.users.find_one({'user_name': username})
        if result:
            if bcrypt.verify(password, result['password']):
                result['_id'] = str(result['_id'])
                return {
                    "success": True,
                    "payload": result
                }
            return {"success": False, "payload": "Wrong password"}
    except Exception as e:
        return {"success": False, "payload": "User Not Found"}



def get_user_by_email(email: str):
    """
    :param email: email for query
    :return: all user info
    """
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        result = db.users.find_one({'email': email})
        if result:
            return {
                "success": True,
                "payload": result
            }
        return {"success": False, "payload": "Not Found"}
    except Exception as e:
        return {"success": False, "payload": e}

def add_friend(username: str, friend: str):
    """
    :param username: username of the user
    :param friend: username of the friend
    :return: success True or False
    """
    try:
        client = DbUsersSystem.get_connection()
        db = client.db
        print(username, friend)
        result_user = db.users.find_one({'user_name': username})
        result_friend = db.users.find_one({'user_name': friend})
        if result_user and result_friend:
            print("HEREEEEE")
            if not result_user.get('friends', []):
                new_friends = [friend]
            else:
                current_friends = result_user['friends']
                if friend in current_friends:
                    return {"success": False, "payload": "Friend is already added"}
                new_friends = result_user['friends'].append(friend)
            db.users.update_one({'user_name': username}, {'$set': {'friends': new_friends}})
            if not result_friend.get('friends', []):
                new_friends = [username]
            else:
                current_friends = result_friend['friends']
                if username in current_friends:
                    return {"success": False, "payload": "Friend is already added"}
                new_friends = result_friend['friends'].append(username)
            return {
                "success": True,
                "payload": "Friend added successfully"
            }
        return {"success": False, "payload": "User or Friend not found"}
    except Exception as e:
        return {"success": False, "payload": e}

def get_all_users():
    """
    :params None
    :return: all users info
    """

    sql = "select * from " + database_name
    result = execute_query(sql=sql)

    if result:
        return {
                "success": True,
                "payload": result
               }
    return {"success": False, "payload": "Not Found" }


def get_user_by_id(user_id: int):
    """

    :param user_id: id for query
    :return: all user info
    """
    sql = "select * from " + database_name + " where _id = %s and disabled = false;"
    result = execute_query(sql=sql, argument=user_id)
    if result:
        return {
                "success": True,
                "payload": result
               }
    return {"success": False, "payload": "Not Found"}


def get_user_by_username(username: str):
    """
    :param username: username of the user
    :return: all user info
    """
    client = DbUsersSystem.get_connection() 
    db = client.db
    result = db.users.find_one({'user_name': username})
    if result:
        result['_id'] = str(result['_id'])
        return {
            "success": True,
            "payload": result
        }
    return {"success": False, "payload": "Not Found"}


def get_user_by_google_id(google_id: str):
    """

    :param google_id: google_id of the user
    :return: all user info
    """
    sql = "select * from " + database_name + " where google_id = %s and disabled = false;"
    result = execute_query(sql=sql, argument=google_id)
    if result:
        return {
                "success": True,
                "payload": result
               }
    return {"success": False, "payload": "Not Found"}


def get_user_by_firstname(firstname: str):
    """

    :param firstname: first name of the user
    :return: all user info
    """
    sql = "select * from " + database_name + " where first_name = %s and disabled = false;"
    result = execute_query(sql=sql, argument=firstname)
    if result:
        return {
            "success": True,
            "payload": result
        }
    return {"success": False, "payload": "Not Found"}


def get_user_by_lastname(lastname: str):
    """
    get_user_by_lastname
    :param lastname: user last name
    :return: all user info
    """
    sql = "select * from " + database_name + " where last_name = %s and disabled = false;"
    result = execute_query(sql=sql, argument=lastname)
    if result:
        return {
            "success": True,
            "payload": result
        }
    return {"success": False, "payload": "Not Found"}


def get_user_liked_books(username: str):
    """
    get_user_by_lastname
    :param username: user last name
    :return: all user info
    """
    sql = "select liked_books from " + database_name + " where user_name = %s and disabled = false;"
    result = execute_query(sql=sql, argument=username)
    if result:
        return {
            "success": True,
            "payload": result
        }
    return {"success": False, "payload": "Not Found"}


def new_user(username: str, password: str, email: str, solidity_address: str, first_name: Optional[str] = None,
             last_name: Optional[str] = None):
    """
    Sends an insert query to the database using execute_query() to create a new User row.
    If email or user_name exist in the database, return 400 with content response.

    :param username: username unique
    :param email: email unique
    :param password: password
    :param first_name: optional first name
    :param last_name: optional surname
    :return: None
    """
    check_user_name = get_user_by_username(username)
    check_email = get_user_by_email(email)
    if check_user_name['success']:
        return {"success": False, "payload": "Error: username already exist"}
    elif check_email['success']:
        return {"success": False, "payload": "Error: email already exist"}

    # Insert user_name, password, email, first_name, last_name, verification_code into the db
    client = DbUsersSystem.get_connection()
    db = client.db
    result = db.users.insert_one({'user_name': username, 'password': password, 'solidity_address': solidity_address, 'email': email, 'first_name': first_name,
                         'last_name': last_name})
    #Store the new user that was just added 
    if result.inserted_id is not None:
        print("Test if we get here!!!")
        new_user = db.users.find_one({'_id': result.inserted_id})
        new_user['_id'] = str(new_user['_id'])
        return {
                "success": True,
                "payload": new_user 
               }

    return {"success": False, "payload": "Couldn't register user"}


# Alter Methods
def add_new_book(username: str, books: str):
    """
        adding new book to the user's liked_books entry
    :param username: username
    :param books: a single book id or list of books id
    :return: success True or False
    """
    sql = "select liked_books from " + database_name + " where user_name = %s;"
    result = execute_query(sql=sql, argument=username)
    if result:
        new_books = ''
        if not result[0]['liked_books']:
            new_books = books
        else:
            current_books = result[0]['liked_books'].split()
            if ' ' in books:
                books_split = books.split()
                for book in books_split:
                    if book in current_books:
                        return {"success": False, "payload": "Book is already liked"}
            else:
                if books in current_books:
                    return {"success": False, "payload": "Book is already liked"}
            new_books = result[0]['liked_books'] + ' ' + books

        new_sql = "update " + database_name + " SET liked_books = %s where user_name = %s;"
        new_result = execute_query(sql=new_sql, argument=(new_books, username))
        return {
            "success": True,
            "payload": new_result
        }
    return {"success": False, "payload": "No books found"}


def remove_book(username: str, books: str):
    """
        removing books from the user liked_books entry.
    :param username: username
    :param books: book ids list or single book id
    :return: success True or False
    """
    sql = "select liked_books from " + database_name + " where user_name = %s;"
    result = execute_query(sql=sql, argument=username)
    if result:
        cur_books = result[0]['liked_books'].replace(books, '')
        new_sql = "update " + database_name + " SET liked_books = %s where user_name = %s;"
        new_result = execute_query(sql=new_sql, argument=(cur_books, username))
        return {
            "success": True,
            "payload": new_result
        }
    return {"success": False, "payload": "No books found"}


def soft_delete_user(username: str, disabled=True):
    """
        soft deletion for a user. Update user disabled entry to equal true
    :param username:
    :return: "success": True if executed or False not.
    """
    try:
        if disabled:
            sql = "update " + database_name + " SET disabled = true where user_name = %s;"
        else:
            sql = "update " + database_name + " SET disabled = false where user_name = %s;"
        result = execute_query(sql=sql, argument=username)

        return {
            "success": True,
            "payload": result
        }
    except Exception as e:
        return {"success": False, "payload": {"Error": e}}


def user_verification(username, verification_code):
    try:
        sql = "select verification_code from " + database_name + " where user_name = %s;"
        result = execute_query(sql=sql, argument=username)

        if not result[0]['verification_code']:
            print("Can't find verification_code")
            raise Exception
        code = result[0]['verification_code']
        if str(code) == verification_code:
            sql = "update " + database_name + " SET email_verified = true where user_name = %s;"
            result = execute_query(sql=sql, argument=username)
            return {
                "success": True,
                "payload": "User is verified"
            }
        else:
            return {
                "success": False,
                "payload": "Wrong verification code"
            }
    except Exception as e:
        return {"success": False, "payload": {"Error": e}}
