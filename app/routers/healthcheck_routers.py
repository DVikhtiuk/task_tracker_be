from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.constants import HEALTHY_HEALTHCHECK_RESPONSE, SELECT_1_Q
from app.core.settings import logger
from app.db.database import async_engine

router = APIRouter(tags=["Health Check"], prefix="/healthcheck")


@router.get("/app")
def app_health_check():
    """
    Health check endpoint to verify if the application is running.

    Returns:
        dict: A response indicating that the application is healthy.
    """
    return HEALTHY_HEALTHCHECK_RESPONSE


@router.get("/db")
async def db_health_check():
    """
    Health check endpoint to verify if the database connection is active.

    Attempts to execute a simple query ("SELECT 1") against the database.
    If the query is successful, the database is considered healthy.

    Returns:
        dict: A response indicating that the database is healthy.

    Raises:
        HTTPException:
            - 500: If the database connection or query fails.
    """
    try:
        async with async_engine.connect() as conn:
            await conn.execute(text(SELECT_1_Q))
        return HEALTHY_HEALTHCHECK_RESPONSE
    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database health check failed",
        )
