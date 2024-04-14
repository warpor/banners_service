import aioredis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.models import User
from api.authentication.user_manager import fastapi_users
from api.banner.crud import get_banner
from api.user_banner import schemas
from database import db_connect, redis_client

router = APIRouter()
current_user = fastapi_users.current_user()


@router.get("/user_banner",
            response_model=schemas.UserBannerReturn)
async def get_user_banner(tag_id: int, feature_id: int,
                          user: User = Depends(current_user),
                          use_last_revision: bool | None = None,
                          redis: aioredis.Redis = Depends(redis_client),
                          db: AsyncSession = Depends(db_connect)):
    banner = await get_banner(db, feature_id, tag_id, use_last_revision, redis)
    if banner.is_active or user.is_superuser:
        return banner
    raise HTTPException(status_code=403, detail="Пользователь не имеет доступа")
