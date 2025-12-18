from sqlalchemy import String, BigInteger, ForeignKey
from src.config.db_config import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from src.models.associations import roles_users
if TYPE_CHECKING:
    from src.models.role import Role
    from src.models.school import School

class User(db.Model):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, autoincrement=True, primary_key=True)
    
    name: Mapped[str] = mapped_column(String(length=80), nullable=False)
    
    email: Mapped[str] = mapped_column(String(length=80), unique=True, nullable=False)
    
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    
    school_id: Mapped[int] = mapped_column(BigInteger, ForeignKey("schools.id"))
    school: Mapped["School"] = relationship(back_populates="users")
    
    roles: Mapped[list["Role"]] = relationship("Role", secondary=roles_users, back_populates="users")
    
    def to_dict(self) -> dict[str, any]: # type: ignore
        return {"id": self.id, "name": self.name, "email": self.email}
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, name='{self.name}')>"
    