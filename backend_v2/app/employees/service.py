from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas import EmployeeCreateModel, EmployeeUpdateModel
from sqlmodel import select, desc
from .models import Employee

class EmployeeService:
    async def get_all_employees(self, session: AsyncSession):
        statement = select(Employee).order_by(desc(Employee.name)) # order_by(desc(Employee.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_a_employee(self, employee_uid:str, session: AsyncSession):
        statement = select(Employee).where(Employee.uid == employee_uid)
        result = await session.exec(statement)
        the_employee =  result.first()
        return the_employee if the_employee is not None else None

    
    async def create_employee(self, employee_data:EmployeeCreateModel, session: AsyncSession):
        employee_data_dict = employee_data.model_dump() # Convert the Pydantic model to a dictionary
        new_employee = Employee(**employee_data_dict) # Create a new Employee instance
        session.add(new_employee)
        await session.commit()
        return new_employee

    async def update_employee(self, employee_uid:str, update_data:EmployeeUpdateModel, session: AsyncSession):
        employee_to_update = await self.get_a_employee(employee_uid, session) # Get the employee to update
        if employee_to_update is not None:
            update_data_dict = update_data.model_dump()
            for key, value in update_data_dict.items():
                setattr(employee_to_update, key, value)
            await session.commit()
            return employee_to_update
        else:
            return None
    

    async def delete_employee(self, employee_uid:str, session: AsyncSession):
        employee_to_delete = await self.get_a_employee(employee_uid, session)

        if employee_to_delete is not None:
            session.delete(employee_to_delete)
            await session.delete(employee_to_delete)
            await session.commit()
            return {"message": "Employee deleted successfully"}
        else:
            return None
