from fastapi import APIRouter, Depends, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.user_manager import super_user
from api.banner import schemas, crud
from database import db_connect

router = APIRouter()


@router.post("/banner",
             response_model=schemas.BannerReturn,
             dependencies=[Depends(super_user)])
async def add_banner(banner: schemas.BannerCreate,
                     db: AsyncSession = Depends(db_connect)):
    return await crud.add_banner(db, banner)


@router.patch("/banner/{banner_id}",
              response_model=schemas.BannerReturn,
              dependencies=[Depends(super_user)]
              )
async def update_banner(banner: schemas.BannerPatch,
                        banner_id: int,
                        db: AsyncSession = Depends(db_connect)):
    if not banner.model_dump(exclude_unset=True):
        return schemas.BannerReturn(id=banner_id)
    return await crud.update_banner(db, banner, banner_id)


@router.delete("/banner/{banner_id}",
               dependencies=[Depends(super_user)],
               )
async def delete_banner(banner_id: int,
                        background_tasks: BackgroundTasks,
                        db: AsyncSession = Depends(db_connect)):
    return await crud.delete_banner(db, banner_id, background_tasks)


@router.get("/banner",
            dependencies=[Depends(super_user)],
            response_model=list[schemas.BannerReturn])
async def get_banners(feature_id: int | None = None,
                      tag_id: int | None = None,
                      limit: int | None = None,
                      offset: int | None = None,
                      db: AsyncSession = Depends(db_connect)):
    return await crud.get_banners(db, feature_id, tag_id, limit, offset)
