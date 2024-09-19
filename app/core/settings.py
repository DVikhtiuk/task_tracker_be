import logging
import sys

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuration settings for the FastAPI application and database connection.

    Attributes:
        APP_HOST (str): The host address where the FastAPI app will run.
        APP_PORT (int): The port number for the FastAPI app.
        DB_USER (str): The username for the PostgreSQL database.
        DB_PASSWORD (str): The password for the PostgreSQL database.
        DB_HOST (str): The host address for the PostgreSQL database.
        DB_PORT (int): The port number for the PostgreSQL database.
        DB_NAME (str): The name of the PostgreSQL database.
        SECRET_KEY (str): The secret key used for JWT token encoding/decoding.
        ALGORITHM (str): The algorithm used for JWT encoding.
    """

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
        """
        Configuration for Pydantic settings.

        Attributes:
            env_file (str): Path to the .env file to load environment variables from.
        """

        env_file = ".env"


settings = Settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)
