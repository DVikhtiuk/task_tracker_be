from fastapi import APIRouter, HTTPException, status
from sqlalchemy import text

from app.constants import HEALTHY_HEALTHCHECK_RESPONSE, SELECT_1_Q
from app.core.settings import logger
from app.db.database import async_engine

router = APIRouter(tags=["Health Check"], prefix="/healthcheck")


@router.get("/app")
def app_health_check():
    return HEALTHY_HEALTHCHECK_RESPONSE


@router.get("/db")
async def db_health_check():
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
