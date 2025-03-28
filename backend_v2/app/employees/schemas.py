from pydantic import BaseModel
from datetime import datetime
import uuid


class Employee(BaseModel):
    uid:uuid.UUID
    name:str
    age:int
    department:str
    salary:float
    created_at:datetime
    updated_at:datetime


class EmployeeCreateModel(BaseModel):
    name:str
    age:int
    department:str
    salary:float



class EmployeeUpdateModel(BaseModel):
    name:str
    age:int
    department:str
    salary:float