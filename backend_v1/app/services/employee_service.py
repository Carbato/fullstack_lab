# Example usage in service layer
from app.core.database import get_db

"""def create_employee(employee_data: EmployeeCreate):
    with next(get_db()) as db:  # Using context manager
        try:
            db_employee = Employee(**employee_data.dict())
            db.add(db_employee)
            db.commit()
            db.refresh(db_employee)
            return db_employee
        except Exception as e:
            db.rollback()
            raise e
"""