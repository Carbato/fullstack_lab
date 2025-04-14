from pydantic import BaseModel, Field
from app.samples.schemas_spl import Sample
from datetime import datetime
from typing import List
import uuid

class UserCreateModel(BaseModel):
    username: str = Field(max_length=8)
    password: str = Field(min_length=6)
    email: str = Field(max_length=40)
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)


class UserModel(BaseModel):
    uid:uuid.UUID
    username:str
    email:str
    first_name:str
    last_name:str
    is_verified:bool
    password_hash:str = Field(exclude=True)  # This will exclude the password from the response
    created_at:datetime 
    updated_at:datetime 


class UserSamplesModel(UserModel):
    samples:List[Sample] 


class UserLoginModel(BaseModel):
    email: str = Field(max_length=40)
    password: str = Field(min_length=6)