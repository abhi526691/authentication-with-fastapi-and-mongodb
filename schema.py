from typing import Optional
from pydantic import BaseModel, EmailStr, Field, SecretStr, conint, root_validator
from db import pymongoObj

class Registration(BaseModel):
    username : str
    email : EmailStr
    password : str = Field(min_length=6)
    confirm_password : str = Field(min_length=6)
    phone : int

    @root_validator
    def verify_password(cls, values):
        password = values.get('password')
        confirm_password = values.get('confirm_password')
        if password != confirm_password:
            raise ValueError("The two password doesnot match")

        return values
    
    @root_validator
    def email_checker(cls, values):
        email = values.get("email")
        if pymongoObj.authentication.register.find_one({"email" : email}):
            raise ValueError("This email is already been used")
        return values
    
    @root_validator
    def phone_checker(cls, values):
        phone = values.get("phone")
        if pymongoObj.authentication.register.find_one({"phone" : phone}):
            raise ValueError("This phone is already been used")
        return values

    @root_validator
    def check_number(cls, values):
        number = values.get("phone")
        if len(str(number)) != 10:
            raise ValueError("Phone number is not valid")
        return values




        
