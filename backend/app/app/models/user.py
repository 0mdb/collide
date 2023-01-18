from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from sqlalchemy.orm import relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from .item import Item  # noqa: F401


class User(SQLAlchemyBaseUserTableUUID, Base):
    pass
    # items = relationship("Item", back_populates="owner")
