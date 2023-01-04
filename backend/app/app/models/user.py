from fastapi_users.db import SQLAlchemyBaseUserTableUUID
from sqlalchemy.ext.declarative import DeclarativeMeta, declarative_base

Base: DeclarativeMeta = declarative_base()


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
    # full_name = Column(String, index=True)
