import os
from typing import Optional, Any, Dict

from pydantic_settings import BaseSettings
from pydantic import AnyUrl, validator

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SERVER_NAME: str
    SERVER_HOST: Any

    # Secret key for encoding and decoding JWTs
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # The token expires in one hour

    # Database configurations for MySQL
    MYSQL_SERVER: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_DB: str
    MYSQL_PORT: int = 3306  # default MySQL port
    SQLALCHEMY_DATABASE_URI: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        
        user = values.get("MYSQL_USER")
        password = values.get("MYSQL_PASSWORD")
        host = values.get("MYSQL_SERVER")
        port = values.get("MYSQL_PORT")
        db = values.get('MYSQL_DB') or ''

        return f"mysql+pymysql://{user}:{password}@{host}:{port}/{db}"

    # Cache configurations
    CACHE_TTL: int = 300  # 5 minutes in seconds

    class Config:
        case_sensitive = True

settings = Settings(
    SERVER_NAME=os.getenv("SERVER_NAME"),
    SERVER_HOST=os.getenv("SERVER_HOST"),
    SECRET_KEY=os.getenv("SECRET_KEY"),
    MYSQL_SERVER=os.getenv("MYSQL_SERVER"),
    MYSQL_USER=os.getenv("MYSQL_USER"),
    MYSQL_PASSWORD=os.getenv("MYSQL_PASSWORD"),
    MYSQL_DB=os.getenv("MYSQL_DB"),
    MYSQL_PORT=int(os.getenv("MYSQL_PORT", 3306)),  # Ensure port is treated as an integer
    SQLALCHEMY_DATABASE_URI=os.getenv("SQLALCHEMY_DATABASE_URI"),
)
