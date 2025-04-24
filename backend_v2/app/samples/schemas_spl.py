from pydantic import BaseModel
from datetime import datetime   
import uuid

class Sample(BaseModel):
    uid:uuid.UUID
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
    client_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str

    def __repr__(self):
        return f"Sample of client='{self.client_uid}', type={self.sample_type}, animal={self.animal}"


class SampleUpdateModel(BaseModel):
    client_uid:uuid.UUID
    user_uid:uuid.UUID
    sample_type:str
    animal:str
    date_reception:datetime
    date_taken:datetime
    state:str

    def __repr__(self):
        return f"Sample of client='{self.client_uid}', type={self.sample_type}, animal={self.animal}"