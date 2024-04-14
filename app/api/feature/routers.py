from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.user_manager import super_user
from api.feature import schemas, crud
from database import db_connect

router = APIRouter()


@router.post("/feature",
             response_model=schemas.FeatureCreate,
             dependencies=[Depends(super_user)]
             )
async def add_feature(feature: schemas.FeatureCreate,
                      db: AsyncSession = Depends(db_connect)):
    return await crud.add_feature(db, feature)
