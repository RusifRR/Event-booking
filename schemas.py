from fastapi import Form
from pydantic import BaseModel, EmailStr


class RegisterForm(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str = Form(min_length=8)
    

class LoginForm(BaseModel):
    email: EmailStr
    password: str = Form(min_length=8)
    