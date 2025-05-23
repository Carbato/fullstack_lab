from passlib.context import CryptContext
from datetime import timedelta, datetime, timezone
from app.config import Config
import jwt
import uuid

passwd_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRE_MINUTES = 1  # Token expiration time in minutes

def generate_passwd_hash(password: str) -> str:
    """
    Generate a hashed password using bcrypt.
    """
    hash = passwd_context.hash(password)
    return hash


def verify_passwd_hash(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a hashed password using bcrypt.
    """
    return passwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expires_delta: timedelta = None, refresh_token: bool = False) -> str:
    payload = {}
    payload["user"] = user_data
    if expires_delta is not None:
        payload["exp"] = datetime.now(timezone.utc) + expires_delta
    else:
        payload["exp"] = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload['jti'] = str(uuid.uuid4())  # Unique identifier for the token
    payload['refresh'] = refresh_token  # Indicates if the token is a refresh token

    token = jwt.encode(
        payload= payload,
        key= Config.JWT_SECRET_KEY,
        algorithm= Config.JWT_ALGORITHM,
    )
    return token


def decode_access_token(token: str) -> dict:
    """
    Decode the access token and return the payload.
    """
    token_data = jwt.decode(
        jwt=token,
        key=Config.JWT_SECRET_KEY,
        algorithms=[Config.JWT_ALGORITHM]
    )
    return token_data