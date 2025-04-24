from sqlmodel.ext.asyncio.session import AsyncSession
from .schemas_his import CreateHistoryModel
from sqlmodel import select, desc
from app.db.models import History
from datetime import datetime

class HistoryService:
    async def get_all_history(self, session: AsyncSession):
        statement = select(History).order_by(desc(History.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_newest_history(self, date_limit:datetime, session: AsyncSession):
        statement = select(History).where(History.created_at >= date_limit).order_by(desc(History.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_oldest_history(self, date_limit:datetime, session: AsyncSession):
        statement = select(History).where(History.created_at <= date_limit).order_by(desc(History.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_user_history(self, user_uid:str, session:AsyncSession):
        statement = select(History).where(History.user_uid == user_uid).order_by(desc(History.created_at))
        result = await session.exec(statement)
        return result.all()
    
    async def get_a_history(self, uid:str, session:AsyncSession):
        statement = select(History).where(History.uid == uid).order_by(desc(History.created_at))
        result = await session.exec(statement)
        return result.first()
    
    async def create_a_history(self, history_data:CreateHistoryModel, session:AsyncSession):
        history_data_dict = history_data.model_dump()
        new_history = History(**history_data_dict)
        session.add(new_history)
        await session.commit()
        return new_history
    
    async def delete_history_from_date(self, date_limit:datetime, session: AsyncSession):
        history_to_delete = await self.get_oldest_history(date_limit, session)
        
        if history_to_delete is not None:
            for history in history_to_delete:
                await session.delete(history)
            
            await session.commit()
            return True
        else:
            return None

