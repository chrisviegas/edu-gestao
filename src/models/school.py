from sqlalchemy import String, BigInteger, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from src.config.db_config import db
from src.domain.address import Address
from src.domain.enums.school_type import SchoolType

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.user import User

class School(db.Model):
    __tablename__ = "schools"
    
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    
    name: Mapped[str] = mapped_column(String(250), nullable=False)
    
    address_street: Mapped[str] = mapped_column(String(120), nullable=True)
    address_number: Mapped[str] = mapped_column(String(20), nullable=True)
    address_neighborhood: Mapped[str] = mapped_column(String(80), nullable=True)
    address_city: Mapped[str] = mapped_column(String(80), nullable=True)
    address_state: Mapped[str] = mapped_column(String(2), nullable=True)
    address_zip_code: Mapped[str] = mapped_column(String(10), nullable=True)

    address = composite(
        Address,
        address_street,
        address_number,
        address_neighborhood,
        address_city,
        address_state,
        address_zip_code,
    )
    
    school_type: Mapped[SchoolType] = mapped_column(Enum(SchoolType, name="school_type_enum", values_callable=lambda e: [m.value for m in e], validate_strings=True), nullable=False)
    
    users: Mapped[list["User"]] = relationship(back_populates="school")
