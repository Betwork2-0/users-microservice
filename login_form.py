from pydantic import BaseModel
from passlib.context import CryptContext
from typing import Optional, Union
import db_util
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, Depends, HTTPException


# openssl rand -hex 32
SECRET_KEY = '1d300c5eea1e16e1158ebb929b3b7d3c633266b298764b02eceab097c8f0b48f'
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/users/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_user(username: str, password: str) -> Union[db_util.User, bool]:
    user = db_util.get_user_by_username(username)['payload'][0]
    print(user)
    print("type::::::", type(user))
    if not user:
        return False
    if not verify_password(password, user['password']):
        return False
    return user


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = db_util.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


