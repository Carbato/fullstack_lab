from sqlmodel import SQLModel, Field, Column  # This is the base class for all models
import sqlalchemy.dialects.postgresql as pg # This is the dialect for PostgreSQL
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
    first_name:str
    last_name:str
    role: str = Field(sa_column=Column(pg.VARCHAR(50) , nullable=False, server_default="user"))  
    is_verified:bool = Field(default=False) 
    password_hash:str = Field(exclude=True)  # This will exclude the password from the response
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))


def __repr__(self):
    return f"<User {self.username}>"  # This will return the name of the user when the object is printed
