from pydantic import BaseModel  
  
class User(BaseModel):  
  username: str | None = None  
  email: str | None = None  
  role: str | None = None  
  disabled: bool| None = None  
  hashed_password: str | None = None  
  
class Token(BaseModel):  
  access_token: str | None = None  
  refresh_token: str | None = None