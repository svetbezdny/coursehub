from fastapi import APIRouter, status

from app.dependencies import AuthServiceDep, UserServiceDep
from app.schemas import TokenRead, UserCreate, UserLogin, UserRead

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_in: UserCreate,
    service: UserServiceDep,
) -> UserRead:
    user = await service.register_user(user_in)
    return UserRead.model_validate(user)


@router.post("/login", response_model=TokenRead)
async def login(
    login_in: UserLogin,
    service: AuthServiceDep,
) -> TokenRead:
    return await service.login(login_in)
