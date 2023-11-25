from fastapi import APIRouter, status, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm
import db_util
from datetime import datetime, timedelta
from passlib.hash import bcrypt
from fastapi.responses import JSONResponse
import login_form
users_info_router = APIRouter(prefix='/api/v1/nba')
#nba_info_router = APIRouter(prefix='/api/v1/nba')
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@users_info_router.get(path='/all-nba-games', status_code=status.HTTP_200_OK, operation_id='get_all_nba_games')
def get_all_nba_games(response: Response):
    """
    return all NBA games that a user can bet on at the current time
    """
    return [{'id':1, 'homeTeam':'LAL', 'awayTeam':'CHI','timeDate': 'test_time', 'homeMoneyLine': '-150', 'awayMoneyLine': '110'}] 
        

@users_info_router.get(path='/test', status_code=status.HTTP_200_OK, operation_id='get_all_users')
def get_user_info_by_id(response: Response):
    """
    return all users
    """
    try:
        return db_util.get_all_users()
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get(path='/user_id/{user_id}', status_code=status.HTTP_200_OK, operation_id='get_user_info_by_id')
def get_user_info_by_id(user_id: int, response: Response):
    """
    return all user info by id
    """
    try:
        return db_util.get_user_by_id(user_id=user_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get(path='/email/{email}', status_code=status.HTTP_200_OK, operation_id='get_user_info_by_email')
def get_user_info_by_email(email: str, response: Response):
    """
    return all user info by email address
    """
    try:
        email = email.lower()
        email.replace('%40', '@')
        return db_util.get_user_by_email(email=email)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get(path='/google_id/{google_id}', status_code=status.HTTP_200_OK,
                       operation_id='get_user_info_by_google_id')
def get_user_info_by_google_id(google_id: str, response: Response):
    """
    return all user info by their google id
    """
    try:
        google_id = google_id.lower()
        return db_util.get_user_by_google_id(google_id=google_id)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get(path='/user_name/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='get_user_info_by_user_name')
def get_user_info_by_user_name(user_name: str, response: Response):
    """
    return all user info by the user_name
    """
    try:
        user_name = user_name.lower()
        return db_util.get_user_by_username(username=user_name)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get(path='/get_books/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='get_user_books')
def get_user_books(user_name: str, response: Response):
    """
    return all user info by the user_name
    """
    try:
        user_name = user_name.lower()
        return db_util.get_user_liked_books(username=user_name)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}

###############################################################################################################
#             PUT methods
###############################################################################################################


@users_info_router.put(path='/user_name/add_book/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='add_new_books_for_user')
def add_new_books_for_user(user_name: str, books: str, response: Response):
    """
    return all user info by the user_name
    """
    try:
        user_name = user_name.lower()
        return db_util.add_new_book(username=user_name, books=books)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.put(path='/user_name/remove_book/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='remove_book_for_user')
def remove_book_for_user(user_name: str, books: str, response: Response):
    """
    return all user info by the user_name
    """
    try:
        user_name = user_name.lower()
        return db_util.remove_book(username=user_name, books=books)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.put(path='/user_name/delete_user/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='soft_delete_user')
def soft_delete_user(user_name: str, user_status: db_util.UserSoftDelete, response: Response):
    """
    return all user info by the user_name
    """
    try:
        user_name = user_name.lower()
        disabled = user_status.disable
        return db_util.soft_delete_user(username=user_name, disabled=disabled)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.put(path='/user_name/user_verification/{user_name}', status_code=status.HTTP_200_OK,
                       operation_id='user_verification')
def user_verification(user_name: str, code: db_util.VerificationCode, response: Response):
    """
    return all user info by the user_name
    """
    try:
        verification_code = code.verification_code
        return db_util.user_verification(username=user_name, verification_code=verification_code)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}

###############################################################################################################
#             POST methods
###############################################################################################################


@users_info_router.post(path='/signup', status_code=status.HTTP_201_CREATED,
                        operation_id='create_new_user')
def create_new_user(user: db_util.User, response: Response):
    """
    """
    try:
        username = user.user_name
        first_name = user.first_name
        last_name = user.last_name
        email = user.email
        password = bcrypt.hash(user.password)
        return db_util.new_user(username=username, password=password, email=email, first_name=first_name,
                                last_name=last_name)
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


"""
=================================================================================================================
                Login and authentication routes
=================================================================================================================
"""


@users_info_router.post("/token", response_model=login_form.Token)
async def login_for_access_token(response: Response, form_data: OAuth2PasswordRequestForm = Depends()):
    """
    return: access token or exception
    """
    print("Hello World!")
    print(login_form)
    try:
        user = login_form.authenticate_user(form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = login_form.create_access_token(
            data={"sub": user['user_name']}, expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"success": False, "payload": {"Error": e}}


@users_info_router.get("/users/me/", response_model=db_util.User)
async def read_users_me(current_user: db_util.User = Depends(login_form.get_current_user)):
    return current_user


@users_info_router.get("/users/me/items/")
async def read_own_items(current_user: db_util.User = Depends(login_form.get_current_user)):
    return [{"item_id": "Foo", "owner": current_user.user_name}]
