from pydantic import BaseModel, EmailStr
from typing import Optional

# register payload
class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    role:str="user"


# login payload
class LoginSchema(BaseModel):
    email: EmailStr
    password: str


# token response
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

# simple user response for auth routes
class AuthUserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_verified: bool
    role: str

    class Config:
        from_attributes = True