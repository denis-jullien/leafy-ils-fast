from datetime import timedelta  
from typing import Annotated  
  
from fastapi import Depends, FastAPI, HTTPException  
from fastapi.security import OAuth2PasswordRequestForm  
  
from auth import create_token, authenticate_user, RoleChecker, get_current_active_user, validate_refresh_token  
from data import fake_users_db, refresh_tokens  
from models import User, Token  
  
app = FastAPI()  
  
ACCESS_TOKEN_EXPIRE_MINUTES = 20  
REFRESH_TOKEN_EXPIRE_MINUTES = 120  
  
@app.get("/")  
def hello_func():  
  return "Hello World !"  
 
@app.get("/hello")  
def hello_func():  
  return "Hello World"  
 
@app.get("/data")  
def get_data(_: Annotated[bool, Depends(RoleChecker(allowed_roles=["admin"]))]):  
  return {"data": "This is important data"}
  
@app.post("/token")  
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:  
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)  
    if not user:  
        raise HTTPException(status_code=400, detail="Incorrect username or password")  
      
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)  
      
    access_token = create_token(data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires)  
    refresh_token = create_token(data={"sub": user.username, "role": user.role}, expires_delta=refresh_token_expires)  
    refresh_tokens.append(refresh_token)  
    return Token(access_token=access_token, refresh_token=refresh_token)  
  
@app.post("/refresh")  
async def refresh_access_token(token_data: Annotated[tuple[User, str], Depends(validate_refresh_token)]):  
    user, token = token_data  
    access_token = create_token(data={"sub": user.username, "role": user.role}, expires_delta=access_token_expires)  
    refresh_token = create_token(data={"sub": user.username, "role": user.role}, expires_delta=refresh_token_expires)  
  
    refresh_tokens.remove(token)  
    refresh_tokens.append(refresh_token)  
    return Token(access_token=access_token, refresh_token=refresh_token)
  
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]