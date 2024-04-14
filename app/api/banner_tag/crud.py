from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from api.banner_tag import models, schemas
from api.banner_tag.models import BannerTag
from core.functions.database_functions import add_object_without_commit, get_object_by_id


async def add_banner_tag(db: AsyncSession,
                         banner_tag: schemas.BannerTagCreate) \
        -> models.BannerTag:
    return await add_object_without_commit(db, banner_tag, models.BannerTag)


async def add_banner_tags_without_commit(db: AsyncSession,
                                         tag_ids_for_add: list[int],
                                         banner_id: int):
    for each_tag_id in tag_ids_for_add:
        banner_tag = schemas.BannerTagCreate(banner_id=banner_id,
                                             tag_id=each_tag_id)
        await add_banner_tag(db, banner_tag)


async def remove_banner_tags_without_commit_with_history(db: AsyncSession,
                                                         tag_ids_for_delete: list[int],
                                                         banner_id: int):
    x = await db.execute(select(BannerTag).where(
        BannerTag.tag_id.in_(tag_ids_for_delete)
        & (BannerTag.banner_id == banner_id)))

    x = x.scalars()
    print(1)


async def remove_banner_tags_without_commit(db: AsyncSession,
                                            tag_ids_for_delete: list[int],
                                            banner_id: int):
    await db.execute(delete(BannerTag).where(
        BannerTag.tag_id.in_(tag_ids_for_delete)
        & (BannerTag.banner_id == banner_id)))


async def get_banner_tags(db: AsyncSession, banner_tag_id: int) -> BannerTag:
    return await get_object_by_id(db, banner_tag_id, BannerTag)
