# app/models/lab_test.py
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.core.database import Base

class LabTest(Base):
    __tablename__ = "lab_tests"
    
    id = Column(Integer, primary_key=True, index=True)
    test_name = Column(String(100))
    test_code = Column(String(20), unique=True)
    description = Column(Text)
    price = Column(Float)
    turnaround_time = Column(Integer)  # Hours
    client_id = Column(Integer, ForeignKey('clients.id'))
    
    client = relationship("Client", back_populates="tests")
