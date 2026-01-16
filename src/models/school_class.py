from typing import TYPE_CHECKING

from sqlalchemy import Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.config.db_config import db
from src.domain.enums.class_grade import ClassGrade

if TYPE_CHECKING:
    from src.models.school import School


class SchoolClass(db.Model):
    __tablename__ = "school_classes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    capacity: Mapped[int] = mapped_column(Integer, nullable=False, default=30)

    class_grade: Mapped[ClassGrade] = mapped_column(Enum(ClassGrade), nullable=False)

    school_id: Mapped[int] = mapped_column(ForeignKey("schools.id"), nullable=False)
    school: Mapped["School"] = relationship(back_populates="school_classes")
