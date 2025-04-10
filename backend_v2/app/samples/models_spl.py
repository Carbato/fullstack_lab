from sqlmodel import SQLModel, Field, Column  # This is the base class for all models   
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid

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
    cod_ref:str
    client_uid:uuid.UUID
    user_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str
    created_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))

    def __repr__(self):
        return f"<Sample {self.cod_ref}>"