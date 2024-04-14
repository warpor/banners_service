from sqlalchemy.ext.asyncio import AsyncSession

from api.feature import schemas, models
from core.functions.database_functions import add_object


async def add_feature(db: AsyncSession,
                      feature: schemas.FeatureCreate) \
        -> models.Feature:
    return await add_object(db, feature, models.Feature)
