from typing import TYPE_CHECKING

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.orm import Mapped, relationship

from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(SQLAlchemyBaseUserTableUUID, Base):
    oauth_accounts: Mapped["OAuthAccount"] = relationship(
        "OAuthAccount", lazy="joined"
    )
    items = relationship("Item", back_populates="owner")

class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass

