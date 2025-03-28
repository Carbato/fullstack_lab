from fastapi import FastAPI
from app.core.database import init_db
from app.api.v1 import employees, clients, lab_tests

app = FastAPI(
    title="Laboratory Management System",
    description="API for managing laboratory operations",
    version="1.0.0"
)

# Initialize database (development only)
@app.on_event("startup")
async def startup_event():
    init_db()

# Include routers
app.include_router(employees.router, prefix="/api/v1/employees", tags=["employees"])
app.include_router(clients.router, prefix="/api/v1/clients", tags=["clients"])
app.include_router(lab_tests.router, prefix="/api/v1/lab-tests", tags=["lab_tests"])
