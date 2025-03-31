from sqlmodel import SQLModel, Field, Column # This is the base class for all models
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid


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
        return f"<Client {self.first_name}>"  # This will return the name of the client when the object is printed
