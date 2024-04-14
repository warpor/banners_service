from sqlalchemy.ext.asyncio import AsyncSession

from api.tag import schemas, models
from core.functions.database_functions import add_object


async def add_tag(db: AsyncSession,
                  tag: schemas.TagCreate) \
        -> models.Tag:
    return await add_object(db, tag, models.Tag)
