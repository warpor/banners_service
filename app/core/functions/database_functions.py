from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


async def add_object_without_commit(db: AsyncSession, schema_object: BaseModel,
                                    db_model: Base):
    db_object = db_model(**schema_object.model_dump())
    db.add(db_object)
    return db_object


async def add_object(db: AsyncSession, schema_object: BaseModel,
                     db_model: Base) -> Base:
    db_object = await add_object_without_commit(db, schema_object, db_model)
    await db.commit()
    await db.refresh(db_object)
    return db_object


async def get_object_by_id(db: AsyncSession, object_id: int,
                           db_model: Base) -> Base:
    db_object = await db.execute(select(db_model).
                                 where(db_model.id == object_id))
    return db_object.scalars().first()


async def get_object_from_db_with_patch(db_object: Base, patch_schema: type[BaseModel],
                                        patched_data: BaseModel) -> BaseModel:
    stored_object = patch_schema.model_validate(db_object)
    patched_data = patched_data.model_dump(exclude_unset=True)
    patched_object = stored_object.model_copy(update=patched_data)
    return patched_object


async def add_patch_object(db: AsyncSession, object_id: int,
                           db_model: Base, object_for_patch: BaseModel) -> Base:
    await db.execute(update(
        db_model).where(db_model.id == object_id).values(object_for_patch.model_dump()))
    await db.commit()
    updated_object = await get_object_by_id(db, object_id, db_model)
    await db.refresh(updated_object)
    return updated_object


async def delete_object_by_id(db: AsyncSession, object_id: int,
                              db_model: Base) -> Base:
    deleted_object = await db.execute(delete(db_model).where(
        db_model.id == object_id))
    await db.commit()
    return deleted_object
