from fastapi_users_db_sqlalchemy.access_token import (
    SQLAlchemyAccessTokenDatabase,
    SQLAlchemyBaseAccessTokenTableUUID,
)

from app.db.base_class import Base


class AccessToken(SQLAlchemyBaseAccessTokenTableUUID, Base):
    pass
