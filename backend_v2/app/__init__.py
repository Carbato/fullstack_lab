from fastapi import FastAPI
from app.clients.routes import client_router
from app.auth.routes_auth import auth_router
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
    title="Lab API",
    description="A simple API to manage users and clients",
    version= version,
    lifespan=life_span
)

app.include_router(client_router, prefix=f"/api/{version}/clients")
app.include_router(auth_router, prefix=f"/api/{version}/auth")