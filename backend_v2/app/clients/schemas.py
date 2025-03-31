from pydantic import BaseModel
from datetime import datetime
import uuid


class Client(BaseModel):
    uid:uuid.UUID
    name:str
    age:int
    department:str
    salary:float
    created_at:datetime
    updated_at:datetime


class ClientCreateModel(BaseModel):
    name:str
    age:int
    department:str
    salary:float



class ClientUpdateModel(BaseModel):
    name:str
    age:int
    department:str
    salary:float