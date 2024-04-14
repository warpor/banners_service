from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.authentication.user_manager import super_user
from api.tag import crud, schemas
from database import db_connect

router = APIRouter()


@router.post("/tag",
             response_model=schemas.TagCreate,
             dependencies=[Depends(super_user)]
             )
async def add_tag(tag: schemas.TagCreate,
                  db: AsyncSession = Depends(db_connect)):
    return await crud.add_tag(db, tag)
