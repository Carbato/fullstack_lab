from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL : str

    model_config = SettingsConfigDict(   # This is where we define the location of the .env file
        env_file=".env",
        extra="ignore"
    )


Config = Settings()  # This is the instance of the Settings class that we will use to access the settings