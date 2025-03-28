from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import AsyncGenerator

from app.config import Config

async_engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL, 
        echo=True   # This will print the SQL queries that are executed
    )
)

async def init_db() -> None:
    async with async_engine.begin() as conn:
        from app.employees.models import Employee
        await conn.run_sync(SQLModel.metadata.create_all)



async def get_session()->AsyncGenerator[AsyncSession, None]: # This function will return a new session
    Session = async_sessionmaker(  
        bind = async_engine,
        class_=AsyncSession,
        expire_on_commit=False # This will prevent the session from being closed after a commit
    )
    async with Session() as session:
        yield session