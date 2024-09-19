from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.settings import settings


def build_async_db_url() -> str:
    """
    Constructs the asynchronous database URL for connecting to the PostgreSQL database.

    Returns:
        str: The asynchronous database URL formatted for SQLAlchemy.
    """
    return (
        f"postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASSWORD}@{settings.DB_HOST}:{settings.DB_PORT}/"
        f"{settings.DB_NAME}"
    )


# Create an asynchronous SQLAlchemy engine
async_engine = create_async_engine(build_async_db_url(), echo=False)

# Configure a sessionmaker for asynchronous sessions
AsyncSessionLocal = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# Create a base class for declarative models
Base = declarative_base()


async def get_db_session() -> AsyncSession:
    """
    Dependency that provides an asynchronous database session.

    Yields:
        AsyncSession: An instance of the SQLAlchemy asynchronous session.
    """
    async with AsyncSessionLocal() as session:
        yield session
