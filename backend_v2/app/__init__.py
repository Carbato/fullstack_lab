from fastapi import FastAPI
from app.employees.routes import employee_router
from contextlib import asynccontextmanager
from app.db.main_db import init_db


@asynccontextmanager  # This is a context manager that will run asynchronously
async def life_span(app: FastAPI):
    print(f"Server is starting ...")
    await init_db()
    yield   # This is where the application code will run
    print(f"Server is shutting down")

version = "v1"  

app = FastAPI(
    title="Employee API",
    description="A simple API to manage employees",
    version= version,
    lifespan=life_span
)

app.include_router(employee_router, prefix=f"/api/{version}/employees")