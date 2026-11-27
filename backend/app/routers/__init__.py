from app.routers.admin import router as admin_router
from app.routers.auth import router as auth_router
from app.routers.courses import router as courses_router
from app.routers.learning import router as learning_router
from app.routers.lessons import router as lessons_router
from app.routers.reviews import router as reviews_router
from app.routers.system import router as system_router
from app.routers.users import router as user_router

routers = (
    admin_router,
    system_router,
    auth_router,
    user_router,
    courses_router,
    lessons_router,
    learning_router,
    reviews_router,
)

__all__ = ("routers",)
