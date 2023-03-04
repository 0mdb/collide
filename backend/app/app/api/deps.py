from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app import crud, models, schemas
from app.core import security
from app.core.config import settings
from app.core.users import current_active_superuser, current_active_user

# from app.db.session import SessionLocal

uri = "postgresql://postgres:changethis@db:5432/app"
engine = create_engine(uri, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token"
)


# def get_db() -> Generator:
#     try:
#         db = SessionLocal()
#         yield db
#     finally:
#         db.close()




def get_current_active_user(
) -> models.User:
    return current_active_user


def get_current_active_superuser(
) -> models.User:
    return current_active_superuser
