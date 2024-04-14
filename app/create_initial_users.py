import asyncio
import contextlib

from dotenv import load_dotenv
from fastapi_users.exceptions import UserAlreadyExists

from api.authentication.schemas import UserCreate
from api.authentication.user_manager import get_user_db, get_user_manager
from database import db_connect

get_async_session_context = contextlib.asynccontextmanager(db_connect)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)

load_dotenv()


async def create_user(email: str, password: str, is_superuser: bool = False,
                      is_active=True):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(email=email, password=password,
                                   is_superuser=is_superuser, is_active=is_active)
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


async def create_users():
    await create_user("admin@mail.com", "admin", is_superuser=True)
    await create_user("user@mail.com", "user", is_superuser=False)


if __name__ == '__main__':
    asyncio.run(create_users())
