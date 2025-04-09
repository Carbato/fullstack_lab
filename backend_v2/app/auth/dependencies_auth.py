import jwt
from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils_auth import decode_access_token
from app.db.redis import token_in_blocklist
from typing import Union
from sqlmodel.ext.asyncio.session import AsyncSession
from app.db.main_db import get_session
from .service_auth import UserService
from typing import List
from .models_auth import User

user_service = UserService()

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request:Request) -> Union[HTTPAuthorizationCredentials, None] :
        creds = await super().__call__(request)
        token = creds.credentials

        
        try:
            token_data = decode_access_token(token)
            self.verify_token_data(token_data)  # Implement your token validation here
            
            # Check if the token is in the blocklist
            if await token_in_blocklist(token_data["jti"]):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "Token has been revoked",
                        "resolution": "Please log in again to obtain a new token"},
                )
            
            return token_data  # Return the original creds object
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token has expired")
        except jwt.InvalidSignatureError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token signature")
        except jwt.DecodeError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token format")
        

    """def token_valid(self, token: str) -> bool:
        
        token_data = decode_access_token(token)
        print(token_data)
        if token_data is not None:
            return True
        else:
            return False"""
        
    def verify_token_data(self, token_data):
            
        raise NotImplementedError("Subclasses must implement this method")



class AccessTokenBearer(TokenBearer):
    
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data.
        """
        if token_data and token_data.get("refresh"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid token data: please provide an access token"
                )



class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        """
        Verify the token data.
        """
        if token_data and not token_data["refresh"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, 
                detail="Invalid token data: please provide a refresh token"
                )


async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session) 
        ):
    """
    Get the current user from the token.
    """
    user_email =  token_details['user']['email']

    user = await user_service.get_user_by_email(user_email, session)

    return user


class RoleChecker:
    """
    Dependency to check user role.
    """
    def __init__(self, allowed_roles: List[str]) -> None:
        self.allowed_roles = allowed_roles  


    def __call__(self, current_user: User = Depends(get_current_user)):
        
        if current_user.role in self.allowed_roles:
            return True
        else:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )