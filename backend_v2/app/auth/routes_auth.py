from fastapi import APIRouter, Depends, status
from .schemas_auth import UserCreateModel, UserModel, UserLoginModel
from .service_auth import UserService
from app.db.main_db import get_session 
from sqlmodel.ext.asyncio.session import AsyncSession
from fastapi import HTTPException
from .utils_auth import create_access_token, decode_access_token, verify_passwd_hash
from .dependencies_auth import RefreshTokenBearer, AccessTokenBearer, RoleChecker, get_current_user
from fastapi.responses import JSONResponse
from datetime import timedelta, datetime
from app.db.redis import add_jti_to_blocklist


auth_router = APIRouter()
user_service = UserService()        
role_checker = RoleChecker(['admin', 'superuser'])


ACCESS_TOKEN_EXPIRE_MINUTES = 60 # 1 hour
REFRESH_TOKEN_EXPIRE_DAYS = 2 # 2 days


#---------------------- SIGN UP NEW USER ----------------------
@auth_router.post(
        '/signup',
        response_model= UserModel,
        status_code=status.HTTP_201_CREATED,
        )
async def create_user_Account(
    user_data: UserCreateModel,
    session: AsyncSession = Depends(get_session)
    ):
    email = user_data.email
    user_exists = await user_service.user_exists(email, session)  
    if user_exists:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Email already exists'
        )
    new_user = await user_service.create_user(user_data, session)

    return new_user



#---------------------- LOGIN FOR USER ----------------------
@auth_router.post('/login')
async def login_user(
    login_data: UserLoginModel, 
    session: AsyncSession = Depends(get_session)
    ):
    email = login_data.email
    password = login_data.password

    user = await user_service.get_user_by_email(email, session)

    if user is not None:
        password_valid =  verify_passwd_hash(password, user.password_hash)

        if password_valid:
            access_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'user_uid': str(user.uid),
                    'role': user.role,
                },
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                )
            refresh_token = create_access_token(
                user_data= {
                    'email': user.email,
                    'user_uid': str(user.uid),
                },
                refresh_token=True,
                expires_delta=timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
                
            )
            
            return JSONResponse(
                content={
                    'message': 'Login successful',
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                    'user': {
                        'email': user.email,
                        'user_uid': str(user.uid),
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                    }
                },
                status_code=status.HTTP_200_OK
            )
        
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid password'
            )
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid email'
        )



#---------------------- REFRESH ACCESS TOKEN ----------------------
@auth_router.get('/refresh-token')
async def get_new_access_token(
    token_details: dict = Depends(RefreshTokenBearer()
    )):
    expires_timestamp = token_details.get('exp')

    if datetime.fromtimestamp(expires_timestamp) > datetime.now():
        new_access_token =  create_access_token(
            user_data = token_details.get('user'),
        )
        return JSONResponse(content={
            'message': 'Access token refreshed successfully',
            'access_token': new_access_token,
        }, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Invvalid or expired token'
        )



#---------------------- GET USER INFO ----------------------
@auth_router.get('/me')
async def get_user(
    user = Depends(get_current_user),
    _:bool = Depends(role_checker)
    ):
    return user

#-----------------------------------------------------------


@auth_router.get('/logout')
async def revoke_token(token_details: dict = Depends(AccessTokenBearer())):
    
    jti = token_details.get('jti')

    await add_jti_to_blocklist(jti)

    return JSONResponse(
        content={
            'message': 'Logged out: Token revoked successfully'
        },
        status_code=status.HTTP_200_OK
    )



#---------------------- DELETE A USER ----------------------
@auth_router.delete('/delete-user')
async def delete_user(
    user_uid: str,
    session: AsyncSession = Depends(get_session),
    access_token_details: dict = Depends(AccessTokenBearer()),
    _:bool = Depends(role_checker)
):
    deleted_user = await user_service.delete_user(user_uid, session)
    print(access_token_details)
    if deleted_user:
        return JSONResponse(
            content={
                'message': 'User deleted successfully'
            },
            status_code=status.HTTP_200_OK
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )