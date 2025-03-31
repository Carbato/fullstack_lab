from sqlmodel import SQLModel, Field, Column  # This is the base class for all models
import sqlalchemy.dialects.postgresql as pg
import uuid
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "users"
    uid:uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,  # This will create a UUID column in the database
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4 # This will generate a unique identifier for each record
        )
    )  
    username:str
    email:str
    fisrt_name:str
    last_name:str
    is_verified:bool
    created_at:datetime
    updated_at:datetime
