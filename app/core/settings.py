import logging
import sys

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # FastAPI
    APP_HOST: str = "localhost"
    APP_PORT: int = 8000

    # PostgreSQL
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "postgres"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_NAME: str = "postgres"

    # Auth
    SECRET_KEY: str = "your_secret_key"
    ALGORITHM: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
