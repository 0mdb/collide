from psycopg2cffi import compat
compat.register()

from typing import AsyncGenerator, Generator

from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase
#from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base
from app.models import AccessToken, User

# Postgres instance
#engine = create_async_engine(settings.SQLALCHEMY_DATABASE_URI, pool_pre_ping=True)
#async_session_maker = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session_maker = sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session


def create_db_and_tables():
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)


def get_user_db(session: Session = Depends(get_session)):
    yield SQLAlchemyUserDatabase(session, User)


def get_access_token_db(
    session: Session = Depends(get_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


# async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
#     async with async_session_maker() as session:
#         yield session
#
#
# async def create_db_and_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)
#
#
# async def get_user_db(session: AsyncSession = Depends(get_async_session)):
#     yield SQLAlchemyUserDatabase(session, User)
#
#
# async def get_access_token_db(
#     session: AsyncSession = Depends(get_async_session),
# ):
#     yield SQLAlchemyAccessTokenDatabase(session, AccessToken)


# def get_gdb() -> Generator:
#     try:
#         db = Memgraph(host=settings.MEMGRAPH_HOST, port=settings.MEMGRAPH_PORT)
#         yield db
#     finally:
#         pass


# gdb = Memgraph(host=settings.MEMGRAPH_HOST, port=settings.MEMGRAPH_PORT)
#     db.close()
