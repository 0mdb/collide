from psycopg2cffi import compat

compat.register()

from typing import Generator

from fastapi import Depends
from .sql_alchemy_user_database_sync import SQLAlchemyUserDatabaseSync

from fastapi_users_db_sqlalchemy.access_token import SQLAlchemyAccessTokenDatabase

from sqlalchemy.orm import sessionmaker

from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.base import Base
from app.models import AccessToken, User

# Postgres instance
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
session_maker = sessionmaker(engine, class_=Session, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    with session_maker() as session:
        yield session


def create_db_and_tables():
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.create_all)


def get_user_db(session: Session = Depends(get_session)):
    yield SQLAlchemyUserDatabaseSync(session, User)


def get_access_token_db(
    session: Session = Depends(get_session),
):
    yield SQLAlchemyAccessTokenDatabase(session, AccessToken)
