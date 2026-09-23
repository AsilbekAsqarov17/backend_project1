from pydantic import BaseModel, EmailStr, Field
from typing import Literal, Any

class user_define(BaseModel):
    username:str = Field(min_length=3, max_length=50)
    email: EmailStr
    age:int = Field(ge=13,le=100)
    is_active:bool

class column_update(BaseModel):
    column_name : Literal["username", "email", "age", "is_active"]
    value : Any
