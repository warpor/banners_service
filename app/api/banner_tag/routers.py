from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.user_manager import super_user
from api.banner_tag import crud, schemas
from database import db_connect

router = APIRouter()


@router.post("/banner_tag",
             dependencies=[Depends(super_user)],
             response_model=schemas.BannerTagCreate)
async def add_banner_tag(banner_tag: schemas.BannerTagCreate,
                         db: AsyncSession = Depends(db_connect)):
    return await crud.add_banner_tag(db, banner_tag)
