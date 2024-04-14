from typing import AsyncGenerator

import aioredis
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.orm import DeclarativeMeta, declarative_base

from variables import SQLALCHEMY_DATABASE_URL, REDIS_URL

Base: DeclarativeMeta = declarative_base()


class DataBaseCreation:

    def __init__(self, session: type[async_sessionmaker], engine: AsyncEngine):
        self.session_maker = session(engine, class_=AsyncSession,
                                     expire_on_commit=False)

    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        async with self.session_maker() as session:
            yield session


class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def connect(self):
        self.redis = await aioredis.from_url(self.redis_url)

    async def disconnect(self):
        if self.redis:
            self.redis.close()
            await self.redis.wait_closed()

    async def get(self, key: str):
        if not self.redis:
            raise RuntimeError("Redis client is not connected")
        value = await self.redis.get(key)
        return value.decode("utf-8")

    async def __call__(self):
        if not self.redis:
            await self.connect()
        return self.redis


async_engine = create_async_engine(SQLALCHEMY_DATABASE_URL)
db_connect = DataBaseCreation(async_sessionmaker, async_engine)
redis_client = RedisClient(REDIS_URL)
