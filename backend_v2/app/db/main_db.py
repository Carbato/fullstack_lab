from sqlmodel import create_engine, text, SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from app.config import Config


engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL, 
        echo=True   # This will print the SQL queries that are executed
    )
)

async def init_db():
    async with engine.begin() as conn:
        from app.employees.models import Employee
        await conn.run_sync(SQLModel.metadata.create_all)
