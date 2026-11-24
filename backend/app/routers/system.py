from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import check_database_connection, get_session

router = APIRouter(tags=["system"])


@router.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": settings.app_title,
    }


@router.get("/ready")
async def ready(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> dict[str, str]:
    await check_database_connection(session)
    return {
        "status": "ready",
        "service": settings.app_title,
        "database": "ok",
    }


@router.get("/version")
def version() -> dict[str, str]:
    return {
        "name": settings.app_title,
        "version": settings.app_version,
        "environment": settings.environment,
    }
