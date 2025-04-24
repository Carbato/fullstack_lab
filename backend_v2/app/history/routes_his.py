from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas_his import HistoryModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service_his import HistoryService
from app.db.main_db import get_session
from typing import List
from datetime import datetime
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
    token_details: dict = Depends(access_token_bearer)
    ):
    print(token_details)
    history = await history_service.get_all_history(session)
    return history

#---------------------- GET NEWEST HISTORY RECORD ----------------------

@history_router.get(
    "/newest/{date_limit}",
    response_model=List[HistoryModel],
    dependencies=[Depends(role_checker)]
)
async def get_newest_history(
    date_limit:datetime,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ):
    print(token_details)
    history = await history_service.get_newest_history(date_limit, session )
    return history

#---------------------- GET OLDEST HISTORY RECORD ----------------------

@history_router.get(
    "/oldest/{date_limit}",
    response_model=List[HistoryModel],
    dependencies=[Depends(role_checker)]
)
async def get_oldest_history(
    date_limit:datetime,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ):
    print(token_details)
    history = await history_service.get_oldest_history(date_limit, session )
    return history

#---------------------- GET USER HISTORY RECORD ----------------------

@history_router.get(
    "/user/{user_uid}",
    response_model=List[HistoryModel],
    dependencies=[Depends(role_checker)]
)
async def get_user_history(
    user_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    print(token_details)
    history = await history_service.get_user_history(user_uid, session)
    return history


#---------------------- GET A SINGLE HISTORY RECORD ----------------------

@history_router.get(
    "/single/{history_uid}",
    response_model=HistoryModel,
    dependencies=[Depends(role_checker)]
)
async def get_a_history(
    history_uid:str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    print(token_details)
    history = await history_service.get_a_history(history_uid, session)
    return history


#---------------------- DELETE HISTORY FROM DATE ----------------------

@history_router.delete(
    "/{date_limit}",
    dependencies=[Depends(role_checker)],
    status_code=status.HTTP_202_ACCEPTED
)
async def get_a_history(
    date_limit:datetime,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    print(token_details)
    deleted_history = await history_service.delete_history_from_date(date_limit, session)
    if deleted_history:
        return {"message": f"History before {str(date_limit)} deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History not found")