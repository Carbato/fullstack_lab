from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas_his import HistoryModel, CreateHistoryModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service_his import HistoryService
from app.db.main_db import get_session
from typing import List
from app.auth.dependencies_auth import AccessTokenBearer, RoleChecker

history_router = APIRouter()
history_service = HistoryService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(['admin', 'superuser'])

#---------------------- GET ALL HISTORY RECORD ----------------------

@history_router.get(
    "/",
    response_model=List[HistoryModel],
    dependencies=[Depends(role_checker)]
)
async def get_all_history(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(AccessTokenBearer)
    ):
    print(token_details)
    history = await history_service.get_all_history(session)
    return history

