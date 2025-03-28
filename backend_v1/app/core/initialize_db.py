# Add this at the top of initialdb.py
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# initial_setup.py
from app.core.database import Base, engine

def initialize_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    initialize_database()