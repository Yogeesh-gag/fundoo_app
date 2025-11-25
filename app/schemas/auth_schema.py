from pydantic import BaseModel, EmailStr,field_validator
from typing import Optional
import re

# register payload
class RegisterSchema(BaseModel):
    name: str
    email: EmailStr
    password: str
    age: Optional[int] = None
    role:str="user"

    @field_validator("name")
    def validate_name(cls, v):
        if not re.fullmatch(r"[A-Za-z ]{3,}", v):
            raise ValueError("Name must be at least 3 letters and contain only alphabets/spaces")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        # Regex: min 8 chars, upper, lower, digit, special char
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$!#%*?&]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must be 8+ chars with upper, lower, number & special char"
            )
        return v

    @field_validator("age")
    def validate_age(cls, v):
        if v is not None and not (1 <= v <= 120):
            raise ValueError("Age must be between 1 and 120")
        return v


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