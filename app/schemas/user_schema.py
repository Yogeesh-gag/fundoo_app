from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional,Literal
import re


class UserBase(BaseModel):
    name: str
    email: EmailStr
    age: Optional[int] = None

class UserCreate(UserBase):
    password: str
    age: int
    role: Literal["user", "admin"] = "user"

    @field_validator("name")
    def validate_name(cls, v):
        # Only letters/spaces, and at least 3 chars
        if not re.fullmatch(r"[A-Za-z ]{3,}", v):
            raise ValueError("Name must be at least 3 letters and contain only alphabets/spaces")
        return v

    @field_validator("password")
    def validate_password(cls, v):
        # Min 8, upper, lower, digit, special char
        pattern = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!#%*?&])[A-Za-z\d@$!#%*?&]{8,}$"
        if not re.match(pattern, v):
            raise ValueError(
                "Password must be 8+ chars with upper, lower, number & special char"
            )
        return v

    @field_validator("age")
    def validate_age(cls, v):
        if not (1 <= v <= 120):
            raise ValueError("Age must be between 1 and 120")
        return v

class UserUpdate(UserBase):
    password:Optional[str]=None

class UserResponse(UserBase):
    id: int
    name: str
    email: EmailStr
    age: int
    role: str
    is_verified:bool

    class Config:
        orm_mode = True
