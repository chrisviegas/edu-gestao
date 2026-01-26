from datetime import datetime
from typing import Optional, List, Dict, Any


from src.config.db_config import db
from src.models.school import School
from src.domain.enums.school_type import SchoolType


class SchoolRepository:
    @staticmethod
    def find_by_id(school_id: int, include_deleted: bool = False) -> Optional[School]:
        """Find a school by its ID.

        Args:
            school_id: School's unique identifier.
            include_deleted: Whether to include soft-deleted schools.

        Returns:
            School object if found, None otherwise.
        """
        query = db.session.query(School).filter(School.id == school_id)

        if not include_deleted:
            query = query.filter(School.deleted_at.is_(None))

        return query.first()

    @staticmethod
    def create_school(
        name: str,
        address_street: str,
        address_number: str,
        address_neighborhood: str,
        address_city: str,
        address_state: str,
        address_zip_code: str,
        school_type: SchoolType,
    ) -> School:
        """Create a new school.

        Args:
            name: School name.
            address_street: Street address.
            address_number: Address number.
            address_neighborhood: Neighborhood.
            address_city: City.
            address_state: State (2-letter code).
            address_zip_code: ZIP code.
            school_type: Type of school (federal, estadual, municipal, privada).

        Returns:
            Created School object.
        """
        school = School()
        school.name = name
        school.address_street = address_street
        school.address_number = address_number
        school.address_neighborhood = address_neighborhood
        school.address_city = address_city
        school.address_state = address_state
        school.address_zip_code = address_zip_code
        school.school_type = school_type

        db.session.add(school)
        db.session.commit()
        return school

    @staticmethod
    def update_school(school_id: int, **kwargs) -> Optional[School]:
        """Update school fields.

        Args:
            school_id: School's unique identifier.
            **kwargs: Fields to update.

        Returns:
            Updated School object if found, None otherwise.
        """
        school = SchoolRepository.find_by_id(school_id)

        if not school:
            return None

        # Update only allowed fields
        allowed_fields = {
            "name",
            "address_street",
            "address_number",
            "address_neighborhood",
            "address_city",
            "address_state",
            "address_zip_code",
            "school_type",
        }

        for field, value in kwargs.items():
            if field in allowed_fields:
                setattr(school, field, value)

        db.session.commit()
        return school

    @staticmethod
    def soft_delete_school(school_id: int) -> bool:
        """Soft delete a school by setting deleted_at timestamp.

        Args:
            school_id: School's unique identifier.

        Returns:
            True if school was deleted, False if not found.
        """
        school = SchoolRepository.find_by_id(school_id, include_deleted=False)

        if not school:
            return False

        school.deleted_at = datetime.utcnow()
        db.session.commit()
        return True

    @staticmethod
    def restore_school(school_id: int) -> bool:
        """Restore a soft-deleted school.

        Args:
            school_id: School's unique identifier.

        Returns:
            True if school was restored, False if not found.
        """
        school = (
            db.session.query(School)
            .filter(School.id == school_id, School.deleted_at.isnot(None))
            .first()
        )

        if not school:
            return False

        school.deleted_at = None
        db.session.commit()
        return True

    @staticmethod
    def get_paginated_schools(
        page: int = 1, per_page: int = 20, include_deleted: bool = False
    ) -> Dict[str, Any]:
        """Get paginated list of schools.

        Args:
            page: Page number (1-based).
            per_page: Items per page.
            include_deleted: Whether to include soft-deleted schools.

        Returns:
            Dictionary with schools list and pagination info.
        """
        page = max(1, int(page))
        per_page = min(max(1, int(per_page)), 100)  # Max 100 per page

        query = db.session.query(School)

        if not include_deleted:
            query = query.filter(School.deleted_at.is_(None))

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "schools": paginated.items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages,
                "has_next": paginated.has_next,
                "has_prev": paginated.has_prev,
            },
        }

    @staticmethod
    def get_schools_by_type_paginated(
        school_type: SchoolType,
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> Dict[str, Any]:
        """Get paginated list of schools filtered by type.

        Args:
            school_type: School type to filter by.
            page: Page number (1-based).
            per_page: Items per page.
            include_deleted: Whether to include soft-deleted schools.

        Returns:
            Dictionary with schools list and pagination info.
        """
        page = max(1, int(page))
        per_page = min(max(1, int(per_page)), 100)  # Max 100 per page

        query = db.session.query(School).filter(School.school_type == school_type)

        if not include_deleted:
            query = query.filter(School.deleted_at.is_(None))

        paginated = query.paginate(page=page, per_page=per_page, error_out=False)

        return {
            "schools": paginated.items,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": paginated.total,
                "pages": paginated.pages,
                "has_next": paginated.has_next,
                "has_prev": paginated.has_prev,
            },
        }

    @staticmethod
    def get_all_schools(include_deleted: bool = False) -> List[School]:
        """Get all schools (not paginated).

        Args:
            include_deleted: Whether to include soft-deleted schools.

        Returns:
            List of all School objects.
        """
        query = db.session.query(School)

        if not include_deleted:
            query = query.filter(School.deleted_at.is_(None))

        return query.all()
