from typing import Dict, Any, List, Optional

from src.repositories.school_repository import SchoolRepository
from src.services.auth_service import is_admin_secretaria, get_current_user_school_id
from src.domain.enums.school_type import SchoolType


class SchoolService:
    @staticmethod
    def create_school_with_address(
        name: str, address: Dict[str, str], school_type: str
    ) -> Optional[Dict[str, Any]]:
        """Create a new school with address data.

        Args:
            name: School name.
            address: Dictionary with address fields.
            school_type: School type as string.

        Returns:
            Created school data as dictionary, None if invalid type.
        """
        try:
            school_type_enum = SchoolType(school_type)
        except ValueError:
            return None

        school = SchoolRepository.create_school(
            name=name,
            address_street=address.get("street", ""),
            address_number=address.get("number", ""),
            address_neighborhood=address.get("neighborhood", ""),
            address_city=address.get("city", ""),
            address_state=address.get("state", ""),
            address_zip_code=address.get("zip_code", ""),
            school_type=school_type_enum,
        )

        return school.to_dict()

    @staticmethod
    def update_school_with_address(
        school_id: int,
        name: Optional[str] = None,
        address: Optional[Dict[str, str]] = None,
        school_type: Optional[str] = None,
    ) -> Optional[Dict[str, Any]]:
        """Update a school with new address data.

        Args:
            school_id: School ID to update.
            name: New school name (optional).
            address: New address dictionary (optional).
            school_type: New school type (optional).

        Returns:
            Updated school data as dictionary, None if not found or invalid type.
        """
        update_data = {}

        if name is not None:
            update_data["name"] = name

        if address is not None:
            update_data.update(
                {
                    "address_street": address.get("street", ""),
                    "address_number": address.get("number", ""),
                    "address_neighborhood": address.get("neighborhood", ""),
                    "address_city": address.get("city", ""),
                    "address_state": address.get("state", ""),
                    "address_zip_code": address.get("zip_code", ""),
                }
            )

        if school_type is not None:
            try:
                school_type_enum = SchoolType(school_type)
                update_data["school_type"] = school_type_enum
            except ValueError:
                return None

        if not update_data:
            return None

        school = SchoolRepository.update_school(school_id, **update_data)

        if school:
            return school.to_dict()

        return None

    @staticmethod
    def get_accessible_schools(
        page: int = 1, per_page: int = 20, include_deleted: bool = False
    ) -> Dict[str, Any]:
        """Get schools based on user permissions.

        Args:
            page: Page number.
            per_page: Items per page.
            include_deleted: Whether to include deleted schools.

        Returns:
            Dictionary with schools and pagination info.
        """
        if is_admin_secretaria():
            # admin_secretaria can see all schools
            return SchoolRepository.get_paginated_schools(
                page=page, per_page=per_page, include_deleted=include_deleted
            )
        else:
            # admin_escola can only see their own school
            user_school_id = get_current_user_school_id()
            if not user_school_id:
                return {
                    "schools": [],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": 0,
                        "pages": 0,
                        "has_next": False,
                        "has_prev": False,
                    },
                }

            school = SchoolRepository.find_by_id(
                user_school_id, include_deleted=include_deleted
            )
            schools = [school] if school else []

            return {
                "schools": schools,
                "pagination": {
                    "page": page,
                    "per_page": per_page,
                    "total": len(schools),
                    "pages": 1,
                    "has_next": False,
                    "has_prev": False,
                },
            }

    @staticmethod
    def validate_school_access(school_id: int) -> bool:
        """Check if current user can access a specific school.

        Args:
            school_id: School ID to check access for.

        Returns:
            True if user has access, False otherwise.
        """
        if is_admin_secretaria():
            return True

        user_school_id = get_current_user_school_id()
        return user_school_id == school_id

    @staticmethod
    def get_accessible_schools_by_type(
        school_type: str,
        page: int = 1,
        per_page: int = 20,
        include_deleted: bool = False,
    ) -> Optional[Dict[str, Any]]:
        """Get schools filtered by type based on user permissions.

        Args:
            school_type: School type to filter by.
            page: Page number.
            per_page: Items per page.
            include_deleted: Whether to include deleted schools.

        Returns:
            Dictionary with schools and pagination info, None if invalid type.
        """
        try:
            school_type_enum = SchoolType(school_type)
        except ValueError:
            return None

        if is_admin_secretaria():
            return SchoolRepository.get_schools_by_type_paginated(
                school_type=school_type_enum,
                page=page,
                per_page=per_page,
                include_deleted=include_deleted,
            )
        else:
            # admin_escola can only see their own school
            user_school_id = get_current_user_school_id()
            if not user_school_id:
                return {
                    "schools": [],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": 0,
                        "pages": 0,
                        "has_next": False,
                        "has_prev": False,
                    },
                }

            school = SchoolRepository.find_by_id(
                user_school_id, include_deleted=include_deleted
            )
            if school and school.school_type == school_type_enum:
                return {
                    "schools": [school],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": 1,
                        "pages": 1,
                        "has_next": False,
                        "has_prev": False,
                    },
                }
            else:
                return {
                    "schools": [],
                    "pagination": {
                        "page": page,
                        "per_page": per_page,
                        "total": 0,
                        "pages": 0,
                        "has_next": False,
                        "has_prev": False,
                    },
                }

    @staticmethod
    def restore_school(school_id: int) -> bool:
        """Restore a soft-deleted school.

        Args:
            school_id: School ID to restore.

        Returns:
            True if school was restored, False otherwise.
        """
        return SchoolRepository.restore_school(school_id)
