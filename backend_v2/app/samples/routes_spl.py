from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from .schemas_spl import Sample, SampleCreateModel, SampleUpdateModel
from sqlmodel.ext.asyncio.session import AsyncSession
from .service_spl import SampleService
from app.db.main_db import get_session
from typing import List
from app.auth.dependencies_auth import AccessTokenBearer, RoleChecker

sample_router = APIRouter()
sample_service = SampleService()
access_token_bearer = AccessTokenBearer()
role_checker = RoleChecker(['admin', 'superuser'])


#---------------------- GET ALL SAMPLES ----------------------
@sample_router.get(
        "/", 
        response_model=List[Sample]
        ) # This will return all samples

async def get_samples(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    ): 
    print(token_details)
    samples = await sample_service.get_all_samples(session) 
    return samples

#---------------------- GET CLIENT SAMPLES ----------------------
@sample_router.get(
        "/client/{client_uid}", 
        response_model=List[Sample]
        ) # This will return all samples

async def get_samples(
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    client_uid:str = None,
    ): 
    print(token_details)
    samples = await sample_service.get_client_samples(client_uid, session)
    return samples

#---------------------- CREATE A SAMPLE ----------------------
@sample_router.post(
        "/",
        status_code=status.HTTP_201_CREATED,
        response_model=Sample,
        dependencies=[Depends(role_checker)]
        ) # This will return the created sample

async def create_a_sample(
    sample_data:SampleCreateModel, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ) -> dict:
    user_uid = token_details.get("user")["user_uid"]

    new_sample = await sample_service.create_sample(user_uid, sample_data, session)

    return new_sample


#---------------------- GET A SAMPLE BY UID ----------------------
@sample_router.get(
        "/{sample_uid}", 
        response_model=Sample
        ) # This will return a single sample

async def get_sample(
    sample_uid:str, 
    session: AsyncSession=Depends(get_session),
    token_details: dict = Depends(access_token_bearer),
    ) -> dict:
    print(token_details)

    the_sample = await sample_service.get_a_sample(sample_uid, session)
    if the_sample:
        return the_sample
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")



#---------------------- UPDATE A SAMPLE ----------------------
@sample_router.put(
        "/{sample_uid}",
        status_code=status.HTTP_202_ACCEPTED,
        response_model=Sample,
        dependencies=[Depends(role_checker)]
        ) # This will return the updated sample

async def update_a_sample(
    sample_uid:str, 
    sample_data:SampleUpdateModel, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ) -> dict:
    print(token_details)

    updated_sample = await sample_service.update_sample(sample_uid, sample_data, session)
    if updated_sample:
        return updated_sample
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")


#---------------------- DELETE A SAMPLE ----------------------
@sample_router.delete(
        "/{sample_uid}",
        status_code=status.HTTP_202_ACCEPTED,
        dependencies=[Depends(role_checker)]
        ) # This will return a message

async def delete_a_sample(
    sample_uid:str, 
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ) -> dict:
    print(token_details)

    deleted_sample = await sample_service.delete_sample(sample_uid, session)
    if deleted_sample:
        return {"message": "Sample deleted successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found")