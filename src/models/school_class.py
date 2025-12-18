from sqlalchemy import String, Integer, BigInteger, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, composite
from src.config.db_config import db
from src.domain.enums.class_grade import ClassGrade

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.models.school import School
class SchoolClass(db.Model):
    __tablename__ = "school_classes"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    
    class_grade: Mapped[ClassGrade] = mapped_column(Enum(ClassGrade, name="class_grade", values_callable=lambda e: [m.value for m in e], validate_strings=True), nullable=False)
    
    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    school: Mapped["School"] = relationship(back_populates="school_classes")