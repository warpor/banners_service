import json
from typing import Sequence

import aioredis
from fastapi import HTTPException, BackgroundTasks
from fastapi.openapi.models import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.banner import schemas, models
from api.banner.classes import TagsForChange
from api.banner.models import Banner
from api.banner_tag.crud import (add_banner_tag, add_banner_tags_without_commit,
                                 remove_banner_tags_without_commit)
from api.banner_tag.models import BannerTag
from api.banner_tag.schemas import BannerTagCreate
from api.user_banner.schemas import UserBannerReturnWithActive
from core.functions.database_functions import (get_object_by_id,
                                               get_object_from_db_with_patch,
                                               add_patch_object, add_object_without_commit, delete_object_by_id,
                                               add_object)
from database import Base


async def update_banner(db: AsyncSession,
                        banner_patch: schemas.BannerPatch,
                        banner_id: int) \
        -> Banner:
    banner_from_db = await get_banner_by_id(db, banner_id)
    if not banner_from_db:
        raise HTTPException(status_code=404, detail="Нет баннера с таким id")
    tags_from_db = get_banner_tags([banner_from_db])

    banner_patch_with_db_data = await get_object_from_db_with_patch(
        banner_from_db, schemas.BannerPatchWithoutTagIds, banner_patch)

    tags_for_change: TagsForChange = await get_banner_tags_for_change(
        db, tags_from_db, banner_patch.tag_ids,
        banner_patch_with_db_data.feature_id,
        banner_from_db.feature_id)

    await update_banner_tags(db, banner_id, tags_for_change)
    return await add_patch_object(db, banner_id,
                                  models.Banner, banner_patch_with_db_data)


async def update_banner_tags(db: AsyncSession, banner_id: int, tags_for_change: TagsForChange):
    await remove_banner_tags_without_commit(
        db, list(tags_for_change.tag_ids_for_delete), banner_id)
    await add_banner_tags_without_commit(db, list(tags_for_change.tag_ids_for_add), banner_id)


def get_banner_tags(banner_from_db: Sequence[Banner]) -> list[int]:
    banner_tag: BannerTag
    return [banner_tag.tag_id for banner in
            banner_from_db for banner_tag in banner.banner_tag]


async def add_banner(db: AsyncSession,
                     banner: schemas.BannerCreate) \
        -> models.Banner:
    if not await check_for_banner_tags_unique(db, banner.tag_ids,
                                              banner.feature_id):
        raise HTTPException(status_code=400, detail="Некорректные данные")
    created_banner = await add_object(db, schemas.BannerDataBaseModel(
        **banner.dict()), models.Banner)
    for each_tag in banner.tag_ids:
        await add_banner_tag(db,
                             BannerTagCreate(banner_id=created_banner.id, tag_id=each_tag))
    await db.commit()
    return created_banner


async def get_banner_by_id(db: AsyncSession, banner_id: int) -> Banner:
    return await get_object_by_id(db, banner_id,
                                  Banner)


async def try_get_banner_from_redis_or_db(db: AsyncSession, redis: aioredis.Redis,
                                          tag_id: int,
                                          feature_id: int):
    key = f"banner:{tag_id}:{feature_id}"
    banner = await redis.hgetall(key)
    if banner:
        return UserBannerReturnWithActive(content=json.loads(banner[b"content"]),
                                          is_active=banner[b"is_active"])
    return await get_banner_with_cache_save(db,
                                            redis, tag_id, feature_id)


async def get_banner_with_cache_save(
        db: AsyncSession,
        redis: aioredis.Redis,
        tag_id: int,
        feature_id: int) -> UserBannerReturnWithActive:
    banner = await get_banner_from_db(db, feature_id, tag_id)
    key = f"banner:{tag_id}:{feature_id}"
    redis_store_info = {"content": json.dumps(banner.content),
                        "is_active": str(banner.is_active)}
    await redis.hset(key, mapping=redis_store_info)
    await redis.expire(key, 5 * 60)
    return UserBannerReturnWithActive(content=banner.content,
                                      is_active=banner.is_active)


async def get_banner_from_db(db: AsyncSession, feature_id: int,
                             tag_id: int) -> models.Banner:
    banner = (await db.execute(select(Banner).where(
        (feature_id == Banner.feature_id) &
        (Banner.banner_tag.any(BannerTag.tag_id == tag_id))))).scalars().first()
    if not banner:
        raise HTTPException(status_code=404, detail="Баннер не найден")
    return banner


async def get_banner(db: AsyncSession, feature_id: int,
                     tag_id: int, use_last_revision,
                     redis: aioredis.Redis) -> UserBannerReturnWithActive:
    if use_last_revision:
        return await get_banner_with_cache_save(db, redis, tag_id, feature_id)

    return await try_get_banner_from_redis_or_db(db, redis, tag_id, feature_id)


async def delete_banner_by_id(db: AsyncSession, banner_id: int) -> Base:
    return await delete_object_by_id(db, banner_id, models.Banner)


async def delete_banner(db: AsyncSession, banner_id: int,
                        background_tasks: BackgroundTasks) -> Response:
    if await get_banner_by_id(db, banner_id):
        background_tasks.add_task(await delete_banner_by_id(db, banner_id))
        return Response(status_code=204, description="Баннер успешно удалён")
    raise HTTPException(status_code=404, detail="Баннер не найден")


async def get_banners(db: AsyncSession, feature_id: int | None = None,
                      tag_id: int | None = None, limit: int | None = None,
                      offset: int | None = None):
    query = select(Banner)

    if feature_id is not None:
        query = query.where(feature_id == Banner.feature_id)

    if tag_id is not None:
        query = query.where(Banner.banner_tag.any(BannerTag.tag_id == tag_id))  # TODO: check

    query = query.offset(offset).limit(limit)
    return (await db.execute(query)).scalars().fetchall()


async def check_for_banner_tags_unique(db: AsyncSession, tag_ids: list[int] | None,
                                       feature_id: int | None) -> bool:
    banners_from_db_by_feature = await get_banners(db, feature_id)
    banner_tag: BannerTag
    tags_in_db = set(get_banner_tags(banners_from_db_by_feature))
    if tags_in_db & set(tag_ids):
        return False
    return True


async def get_banner_tags_for_change(
        db: AsyncSession, tags_from_db: list[int] | None,
        tag_ids_for_patch: list[int] | None, feature_id_from_db: int,
        feature_id_for_patch: int | None) -> TagsForChange:
    tag_ids_for_delete: list[int] = []
    tag_ids_for_add: list[int] = []

    if tag_ids_for_patch is None:
        if ((feature_id_for_patch != feature_id_from_db)
                and not await check_for_banner_tags_unique(db, tags_from_db, feature_id_from_db)):
            raise HTTPException(status_code=400, detail="Некорректные данные")
    else:
        if feature_id_for_patch == feature_id_from_db:
            tag_ids_for_delete = list(set(tags_from_db) - set(tag_ids_for_patch))
            tag_ids_for_add = list(set(tag_ids_for_patch) - set(tags_from_db))
        else:
            tag_ids_for_delete = tag_ids_for_add = tag_ids_for_patch

        if not await check_for_banner_tags_unique(db, list(tag_ids_for_add), feature_id_from_db):
            raise HTTPException(status_code=400, detail="Некорректные данные")

    return TagsForChange(tag_ids_for_add=tag_ids_for_add,
                         tag_ids_for_delete=tag_ids_for_delete)
