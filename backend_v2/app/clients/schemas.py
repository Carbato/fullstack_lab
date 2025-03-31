from pydantic import BaseModel
from datetime import datetime
import uuid


class Client(BaseModel):
    uid:uuid.UUID
    lid:str
    first_name:str
    last_name:str
    email:str
    phone:str
    address:str
    service_count:int
    created_at:datetime
    updated_at:datetime


class ClientCreateModel(BaseModel):
    lid:str
    first_name:str
    last_name:str
    email:str
    phone:str
    address:str
    service_count:int




class ClientUpdateModel(BaseModel):
    email:str
    phone:str
    address:str
    service_count:int
