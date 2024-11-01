from fastapi.security import OAuth2PasswordBearer   
from passlib.context import CryptContext  
from models import User  
# from jose import JWTError, jwt 
import jwt 
from jwt.exceptions import InvalidTokenError

from datetime import datetime, timedelta, timezone  
from data import refresh_tokens  
from typing import Annotated  
from fastapi import Depends, HTTPException, status  
  
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")  
  
  # to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"  
ALGORITHM = "HS256"  
  
def get_user(db, username: str):  
    print(f"user {username} in {db} ?????????")
    if username in db:  
        print("user !!!")
        user = db[username]  
        return User(**user)  
  
  
def authenticate_user(fake_db, username: str, password: str):  
    print(f"user {username}, pass {password}")
    user = get_user(fake_db, username)  
    if not user:  
        return False  
    # if not pwd_context.verify(password, user.hashed_password):  
    #     return False  
    return user  
  
  
def create_token(data: dict, expires_delta: timedelta | None = None):  
    to_encode = data.copy()  
    if expires_delta:  
        expire = datetime.now(timezone.utc) + expires_delta  
    else:  
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)  
    to_encode.update({"exp": expire})  
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)  
    return encoded_jwt  
  
  
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):  
    credentials_exception = HTTPException(  
        status_code=status.HTTP_401_UNAUTHORIZED,  
        detail="Could not validate credentials",  
        headers={"WWW-Authenticate": "Bearer"},  
    )  
    try:  
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
        username: str = payload.get("sub")  
        if username is None:  
            raise credentials_exception  
    except InvalidTokenError:  
        raise credentials_exception  
    user = get_user(fake_users_db, username=username)  
    if user is None:  
        raise credentials_exception  
    return user  
  
  
async def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):  
    if current_user.disabled:  
        raise HTTPException(status_code=400, detail="Inactive user")  
    return current_user  
  
  
async def validate_refresh_token(token: Annotated[str, Depends(oauth2_scheme)]):  
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")  
    try:  
        if token in refresh_tokens:  
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])  
            username: str = payload.get("sub")  
            role: str = payload.get("role")  
            if username is None or role is None:  
                raise credentials_exception  
        else:  
            raise credentials_exception  
  
    except (InvalidTokenError):  
        raise credentials_exception  
    user = get_user(fake_users_db, username=username)  
    if user is None:  
        raise credentials_exception  
    return user, token  
  
  
class RoleChecker:  
  def __init__(self, allowed_roles):  
    self.allowed_roles = allowed_roles  
  
  def __call__(self, user: Annotated[User, Depends(get_current_active_user)]):  
    if user.role in self.allowed_roles:  
      return True  
    raise HTTPException(  
status_code=status.HTTP_401_UNAUTHORIZED,   
detail="You don't have enough permissions")  