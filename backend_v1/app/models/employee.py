# app/models/employee.py
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True)
    position = Column(String(100))
    status = Column(String(20))