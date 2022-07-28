from fastapi import APIRouter
from pydantic import EmailStr
from schema import Registration
from db import pymongoObj


router = APIRouter(
    prefix="/api",
    tags=["api"],
    responses={404: {"description": "Not found"}},
)


@router.post('/register')
def registration(registerObj : Registration):
    try:
        result = {
            "username" : registerObj.username,
            "email" : registerObj.email,
            "password" : registerObj.password,
            "phone" : registerObj.phone
        }
        pymongoObj.authentication.register.insert_one(result)
        return "Registered successfully"
    except Exception as e:
        raise ValueError("Error found in registering the data")


@router.post('/loginwithemail')
def loginwithemail(email:EmailStr, password:str):
    try:
        if pymongoObj.authentication.register.find_one({'email' : email}):
            result = pymongoObj.authentication.register.find_one({'email' : email, 'password' : password})
            if result:
                return "Logged in Successfully"
            else:
                return "Email and password doesnot match"
        else:
            return "This email is not found in our database"
    except Exception as e:
        raise ValueError("Error occured")


@router.post('/loginwithphone')
def loginwithphone(phone:int, password:str):
    try:
        if pymongoObj.authentication.register.find_one({'phone' : phone}):
            result = pymongoObj.authentication.register.find_one({'phone' : phone, 'password' : password})
            if result:
                return "Logged in Successfully"
            else:
                return "Phone number and password doesnot match"
        else:
            return "This phone number is not found in our database"
    except Exception as e:
        raise ValueError("Error occured")



@router.post("/change-password")
def changepassword(email:EmailStr, password: str, confirm_password:str):
    try:
        if password != confirm_password:
            raise ValueError("Password and confirm password doesnot match")
        result = pymongoObj.authentication.register.update_one(
            {"email" : email},
            {"$set" : {"password" : password}
            }
        )
        return "Password changed successfully"
    except Exception as e:
        raise ValueError("Error occured")


    


    