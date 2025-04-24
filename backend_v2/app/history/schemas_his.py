from pydantic import BaseModel
from datetime import datetime
import uuid


class HistoryModel(BaseModel):
    uid:uuid.UUID
    user_uid:uuid.UUID
    action:str
    obj:str
    created_at:datetime

class CreateHistoryModel(BaseModel):
    user_uid:uuid.UUID
    action:str
    obj:str