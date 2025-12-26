from pydantic import BaseModel

class User(BaseModel):
    email:str
    username:str
    password:str


class Post(BaseModel):
    id:int
    title:str
    content:str
