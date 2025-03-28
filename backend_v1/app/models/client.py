# app/models/client.py
from sqlalchemy import Column, Integer, String, Text
from app.core.database import Base

class Client(Base):
    __tablename__ = "clients"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False, unique=True)
    phone = Column(String(20), unique=True)
    address = Column(Text)
    tax_id = Column(String(30), unique=True)
