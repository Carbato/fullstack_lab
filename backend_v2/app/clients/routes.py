from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from app.clients.schemas import Client, ClientCreateModel, ClientUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.clients.service import ClientService 
from app.db.main_db import get_session
from typing import List
from app.auth.dependencies_auth import AccessTokenBearer, RoleChecker

client_router = APIRouter()
client_service = ClientService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(['admin', 'superuser'])

#---------------------- GET ALL CLIENTS ----------------------
@client_router.get(
        "/", 
        response_model=List[Client]
        ) # This will return all clients

async def get_client(
    session: AsyncSession = Depends(get_session),
    user_details= Depends(access_token_bearer),
    ): 
    print(user_details)
    clients = await client_service.get_all_clients(session) 
    return clients


#---------------------- CREATE A CLIENT ----------------------
@client_router.post(
        "/", 
        status_code=status.HTTP_201_CREATED, 
        response_model=Client,
        dependencies=[Depends(role_checker)]
        ) # This will return the created client

async def create_a_client(
    client_data:ClientCreateModel, 
    session: AsyncSession = Depends(get_session),
    user_details= Depends(access_token_bearer),
    ) -> dict:
    print(user_details)

    new_client = await client_service.create_client(client_data, session)
    
    return new_client


#---------------------- GET A CLIENT BY UID ----------------------
@client_router.get(
        "/{client_uid}", 
        response_model=Client
        ) # This will return a single client

async def get_client(
    client_uid:str, 
    session: AsyncSession=Depends(get_session),
    user_details= Depends(access_token_bearer),
    ) -> dict:
    print(user_details)

    client = await client_service.get_a_client(client_uid, session)
    if client:
        return client
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")



#---------------------- UPDATE A CLIENT ----------------------
@client_router.put(
        "/{client_uid}", 
        status_code=status.HTTP_202_ACCEPTED,  
        response_model=Client,
        dependencies=[Depends(role_checker)]
        ) # This will return the updated client

async def update_client(
    client_uid:str, 
    client_update_data:ClientUpdateModel, 
    session: AsyncSession = Depends(get_session),
    user_details= Depends(access_token_bearer),
    ) -> dict:
    print(user_details)

    updated_client = await client_service.update_client(client_uid, client_update_data, session) 
    if updated_client:
        return updated_client
    else:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Client not found")


#---------------------- DELETE A CLIENT ----------------------
@client_router.delete(
        "/{client_uid}", 
        status_code=status.HTTP_202_ACCEPTED,
        dependencies=[Depends(role_checker)],
        ) # This will return the deleted client

async def delete_client(
    client_uid:str,
    session: AsyncSession = Depends(get_session),
    user_details= Depends(access_token_bearer),
    ):
    print(user_details)
    
    client_to_delete = await client_service.delete_client(client_uid, session)
    if client_to_delete:
        return {"message": "Client deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    