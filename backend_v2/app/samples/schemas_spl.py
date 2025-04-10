from pydantic import BaseModel
from datetime import datetime   
import uuid

class Sample(BaseModel):
    uid:uuid.UUID
    cod_ref:str
    client_uid:uuid.UUID
    user_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str
    created_at:datetime
    updated_at:datetime


class SampleCreateModel(BaseModel):
    cod_ref:str
    client_uid:uuid.UUID
    user_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str


class SampleUpdateModel(BaseModel):
    client_uid:uuid.UUID
    user_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str