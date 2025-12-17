from sqlalchemy import String, Integer
from src.config.db_config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.models.associations import roles_users
if TYPE_CHECKING:
    from src.models.user import User

class Role(db.Model):
    __tablename__ = "roles"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    
    users: Mapped[list["User"]] = relationship(
        "User",
        secondary=roles_users,
        back_populates="roles"
    )
