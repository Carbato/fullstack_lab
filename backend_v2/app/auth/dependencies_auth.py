import jwt
from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPBearer
from fastapi.security.http import HTTPAuthorizationCredentials
from .utils_auth import decode_access_token
from app.db.redis import token_in_blocklist
from typing import Union

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
