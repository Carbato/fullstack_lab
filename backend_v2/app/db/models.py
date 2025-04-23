from sqlmodel import SQLModel, Column, Field, Relationship  # This is the base class for all models   
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
from typing import Optional, List
import uuid


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
    samples:List["Sample"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy":"selectin"})  # This will create a relationship with the Sample model 

    def __repr__(self):
        return f"<User {self.username}>"  # This will return the name of the user when the object is printed



class Client(SQLModel, table=True):  # This will create a table in the database
    __tablename__ = "clients"  # This is the name of the table in the database

    uid:uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,  # This will create a UUID column in the database
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4 # This will generate a unique identifier for each record
        )
    )  
    lid:str
    first_name:str
    last_name:str
    email:str
    phone:str
    address:str
    service_count:int
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Client {self.first_name} {self.last_name}>"  # This will return the name of the client when the object is printed



class Sample(SQLModel, table=True):  # This will create a table in the database
    __tablename__ = "samples"  # This is the name of the table in the database

    uid:uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,  # This will create a UUID column in the database
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4 # This will generate a unique identifier for each record
        )
    )
    client_uid:uuid.UUID
    user_uid:Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    user:Optional[User] = Relationship(back_populates="samples") # This will create a relationship with the User model
    
    def __repr__(self):
        return f"<Sample {self.sample_type} with uid {self.uid}>"



class History(SQLModel, table=True):  # This will create a table in the database
    __tablename__ = "history"  # This is the name of the table in the database

    uid:uuid.UUID = Field(
        sa_column= Column(
            pg.UUID,  # This will create a UUID column in the database
            nullable=False, 
            primary_key=True, 
            default=uuid.uuid4 # This will generate a unique identifier for each record
        )
    )
    user_uid:Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid")
    action:str
    obj:str
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<The user {self.user_uid} used the function {self.action} in {self.obj}>"