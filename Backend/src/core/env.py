
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE: str
    NAMEDB: str
    PORT: int = 8000
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        
    @property
    def MONGO_URI(self) -> str:
        return self.DATABASE
    
    @property
    def MONGO_DB_NAME(self) -> str:
        return self.NAMEDB