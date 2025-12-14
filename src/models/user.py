from sqlalchemy import String, BigInteger
from src.config.db_config import db
from flask_login import UserMixin
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    
    name: Mapped[str] = mapped_column(String(length=80), nullable=False)
    
    email: Mapped[str] = mapped_column(String(length=80), unique=True, nullable=False)
    
    hash_password: Mapped[str] = mapped_column(String, nullable=False)
    
    def to_dict(self) -> dict[str, any]:
        return {"id": self.id, "name": self.name, "email": self.email}
    
    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, name='{self.name}')>"
    