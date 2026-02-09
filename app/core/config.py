from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Task app"
    DEBUG: bool = True

    SECRET_KEY: str = "super-secret-key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(env_file = ".env")

    DATABASE_URL: str = "sqlite:///./db.sqlite3"
    

settings = Settings()