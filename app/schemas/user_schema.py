from pydantic import BaseModel, EmailStr, validator
from typing import Optional,Literal

class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(UserBase):
    name: str
    email: EmailStr
    password: str
    age: int
    role: Literal["user", "admin"] = "user"

class UserUpdate(UserBase):
    password:Optional[str]=None

class UserResponse(UserBase):
    id: int
    name: str
    email: EmailStr
    age: int
    role: str

    class Config:
        orm_mode = True
