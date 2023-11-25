# getters
import os
from typing import Optional, Any
from fastapi import status, Response
import pymysql
from pydantic import BaseModel
from passlib.hash import bcrypt
import uuid
from email_verf import send_email


database_name = "users_db.users"
# database_name = "user_test.users"  # for local testing


class VerificationCode(BaseModel):
    verification_code: str


class Books(BaseModel):
    books: str


class UserSoftDelete(BaseModel):
    disable: bool


class User(BaseModel):
    """
        User class model
    """
    user_name: str
    password: str
    email: str
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
        user = "admin"
        password = "the_warriors"
        host = "books.c4m5teyjg8v7.us-east-1.rds.amazonaws.com"
        # testing info
        # user = "root"
        # password = "Revamped1!"
        # host = "localhost"
        try:
            connection = pymysql.connect(user=user,
                                         password=password,
                                         host=host,
                                         cursorclass=pymysql.cursors.DictCursor,
                                         autocommit=True)

        except Exception:
            return None
        return connection




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


def get_user_by_email(email: str):
    """

    :param email: email for query
    :return: all user info
    """
    try:
        sql = "select * from " + database_name + " where email = %s and disabled = false;"
        result = execute_query(sql=sql, argument=email)
        if result:
            return {
                "success": True,
                "payload": result
            }
        return {"success": False, "payload": "Not Found"}
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
    sql = "select * from " + database_name + " where user_name = %s and disabled = false;"
    result = execute_query(sql=sql, argument=username)
    if result:
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


def new_user(username: str, password: str, email: str, first_name: Optional[str] = None,
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

    verification_code = str(uuid.uuid4().hex)
    sql = "INSERT INTO " + database_name + \
          "(user_name, password, email, first_name, last_name, verification_code) VALUES (%s, %s, %s, %s, %s, %s)"
    result = execute_query(sql=sql, argument=(username, password, email, first_name, last_name, verification_code))
    if not result:
        send_email(email, verification_code)  # send email for verification
    if not result:
        return {
                "success": True,
                "payload": result
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
