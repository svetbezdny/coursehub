from fastapi import APIRouter

from app.dependencies import AdminDep, AdminServiceDep
from app.schemas import AdminStatsRead

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/stats", response_model=AdminStatsRead)
async def get_stats(
    _current_user: AdminDep,
    service: AdminServiceDep,
) -> AdminStatsRead:
    return await service.get_stats()
