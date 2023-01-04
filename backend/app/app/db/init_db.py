from sqlalchemy.orm import Session
import asyncio
from app.core.config import settings
from app.models import Base  # noqa: F401
from app.db.session import get_async_session, get_user_db, engine
from app.core.users import get_user_manager
import contextlib
from fastapi_users.exceptions import UserAlreadyExists
from app.schemas import UserCreate
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def create_superuser(email: str, password: str, is_superuser: bool = False):
    try:
        async with get_async_session_context() as session:
            async with get_user_db_context(session) as user_db:
                async with get_user_manager_context(user_db) as user_manager:
                    user = await user_manager.create(
                        UserCreate(
                            email=email, password=password, is_superuser=is_superuser
                        )
                    )
                    print(f"User created {user}")
    except UserAlreadyExists:
        print(f"User {email} already exists")


# make sure all SQL Alchemy models are imported (app.db.base) before initializing DB
# otherwise, SQL Alchemy might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-postgresql/issues/28
async def init_db() -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next line
    await create_db_and_tables()
    await create_superuser(
        email=settings.FIRST_SUPERUSER,
        password=settings.FIRST_SUPERUSER_PASSWORD,
        is_superuser=True,
    )

    # user = crud.user.get_by_email(db, email=settings.FIRST_SUPERUSER)
    # if not user:
    #     user_in = schemas.UserCreate(
    #         email=settings.FIRST_SUPERUSER,
    #         password=settings.FIRST_SUPERUSER_PASSWORD,
    #         is_superuser=True,
    #     )
    #     user = crud.user.create(db, obj_in=user_in)  # noqa: F841
