from pydantic import BaseModel,EmailStr



class UserCreate(BaseModel):
    email:EmailStr
    fullName:str
    password:str
