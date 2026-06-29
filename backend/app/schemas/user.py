from pydantic import BaseModel
from pydantic import EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    mobile: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: str
    email: EmailStr
    mobile: str


class PasswordChange(BaseModel):
    current_password: str
    new_password: str


class UserResponse(BaseModel):
    user_id: int
    name: str
    email: str
    mobile: str

    class Config:
        from_attributes = True
