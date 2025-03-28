from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from app.employees.schemas import Employee, EmployeeUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.employees.service import EmployeeService 
from app.employees.models import Employee
from app.db.main_db import get_session

from typing import List

employee_router = APIRouter()
employee_service = EmployeeService()




@employee_router.get("/", response_model=List[Employee])
async def get_employees(
    session: AsyncSession = Depends(get_session) 
    ):

    employees = await employee_service.get_all_employees(session) # This will return all the employees
    return employees


@employee_router.post("/", status_code=status.HTTP_201_CREATED, response_model=Employee)
async def create_a_employee(
    employee_data:Employee, 
    session: AsyncSession = Depends(get_session)
    ) -> dict:

    new_employee = await employee_service.create_employee(employee_data, session)
    
    return new_employee



@employee_router.get("/{employee_uid}")
async def get_employee(
    employee_uid:int, 
    session: AsyncSession=Depends(get_session)
    ) -> dict:

    employee = await employee_service.get_a_employee(employee_uid, session)
    if employee:
        return employee
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")


@employee_router.put("/{employee_uid}", status_code=status.HTTP_202_ACCEPTED)
async def update_employee(
    employee_uid:int, 
    employee_update_data:EmployeeUpdateModel, 
    session: AsyncSession = Depends(get_session)
    ) -> dict:

    updated_employee = await employee_service.update_employee(employee_uid, employee_update_data, session) 
    if updated_employee:
        return updated_employee
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Employee not found")


@employee_router.delete("/{employee_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(
    employee_uid:int,
    session: AsyncSession = Depends(get_session)
    ):

    employee_to_delete = await employee_service.delete_employee(employee_uid, session)
    if employee_to_delete:
        return None
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
