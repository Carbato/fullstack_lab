from pydantic import BaseSettings, PostgresDsn, validator
from typing import Optional

class Settings(BaseSettings):
    # Application Configuration
    app_env: str = "development"
    app_secret_key: str
    debug: bool = False
    
    # MySQL Configuration
    db_host: str
    db_port: str
    db_user: str
    db_password: str
    db_name: str
    db_pool_size: int = 10
    db_max_overflow: int = 20
    
    # JWT Configuration
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        return f"mysql+mysqlconnector://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

settings = Settings()
