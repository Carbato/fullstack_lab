from fastapi import APIRouter, status, HTTPException
from typing import Optional, List
from app.employees.schemas import Employee

employee_router = APIRouter()

employees = [
    Employee(id=1, name="John Doe", age=30, department="IT", salary=100000),
    Employee(id=2, name="Jane Doe", age=35, department="HR", salary=80000),
    Employee(id=3, name="Tom Smith", age=40, department="Finance", salary=120000),
]




@employee_router.get("/", response_model=List[Employee])
async def get_employees():
    return employees


@employee_router.post("/", status_code=status.HTTP_201_CREATED)
async def add_employee(employee_data:Employee) -> dict:
    
    new_employee = employee_data.model_dump()
    employees.append(new_employee)
    return {
        "message":"Employee added successfully",
        "employees":employees}



@employee_router.get("/{id}")
async def get_employee(id:int):
    for employee in employees:
        if employee.id == id:
            return employee
    raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.put("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def update_employee(employee_data:Employee) -> dict:
    for i in range(len(employees)):
        if employees[i].id == employee_data.id:
            employees[i] = employee_data
            return {"message":"Employee updated"}
    raise HTTPException(status_code=404, detail="Employee not found")


@employee_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(id:int):
    for i in range(len(employees)):
        if employees[i].id == id:
            employees.pop(i)
            return {"message":"Employee deleted"}
    raise HTTPException(status_code=404, detail="Employee not found")
