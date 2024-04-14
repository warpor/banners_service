import uuid

from fastapi_users_db_sqlalchemy.access_token import \
    SQLAlchemyBaseAccessTokenTable
from sqlalchemy import UUID, Column, ForeignKey
from sqlalchemy.orm import declared_attr

from database import Base


class AccessToken(SQLAlchemyBaseAccessTokenTable[uuid.UUID], Base):
    @declared_attr
    def user_id(cls):
        return Column(UUID, ForeignKey("users.id",
                                          ondelete="cascade"), nullable=False)
