from fastapi import Depends, APIRouter

from api.authentication.models import User
from api.authentication.schemas import UserRead, UserCreate
from api.authentication.user_manager import fastapi_users, auth_backend, current_login_user, super_user

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
