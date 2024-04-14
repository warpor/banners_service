from fastapi import Depends
from fastapi_users_db_sqlalchemy.access_token import \
    SQLAlchemyAccessTokenDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from api.tokens.models import AccessToken
from database import db_connect


async def get_access_token_db(session: AsyncSession = Depends(db_connect)):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
