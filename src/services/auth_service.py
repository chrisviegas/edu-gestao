from typing import List, Optional

from flask_jwt_extended import create_access_token, get_jwt_identity

from src.config.db_config import db
from src.models.user import User


def generate_token(user: User) -> str:
    """Generate a JWT access token for a user.

    Args:
        user: User object to generate token for.

    Returns:
        JWT access token string containing user ID, roles, and school_id in claims.
    """
    roles = [role.name for role in user.roles]

    additional_claims = {"roles": roles, "school_id": user.school_id}

    return create_access_token(
        identity=str(user.id), additional_claims=additional_claims
    )


def get_current_user_id() -> Optional[int]:
    """Get the ID of the currently authenticated user from JWT.

    Returns:
        User ID if token is valid, None otherwise.
    """
    try:
        return get_jwt_identity()
    except Exception:
        return None


def get_current_user() -> Optional[User]:
    """Get the currently authenticated user object.

    Returns:
        User object if found, None otherwise.
    """
    user_id = get_current_user_id()
    if user_id:
        return db.session.query(User).filter(User.id == user_id).first()
    return None


def get_current_user_roles() -> List[str]:
    """Get the list of roles assigned to the current user.

    Returns:
        List of role names from JWT claims, empty list if not found.
    """
    from flask_jwt_extended import get_jwt

    try:
        claims = get_jwt()
        return claims.get("roles", [])
    except Exception:
        return []


def get_current_user_school_id() -> Optional[int]:
    """Get the school ID of the currently authenticated user.

    Returns:
        School ID from JWT claims, None otherwise.
    """
    from flask_jwt_extended import get_jwt

    try:
        claims = get_jwt()
        return claims.get("school_id")
    except Exception:
        return None


def has_role(role_name: str) -> bool:
    """Check if current user has a specific role.

    Args:
        role_name: Name of role to check.

    Returns:
        True if user has the role, False otherwise.
    """
    return role_name in get_current_user_roles()


def has_any_role(*role_names: str) -> bool:
    """Check if current user has any of the specified roles.

    Args:
        *role_names: Variable number of role names to check.

    Returns:
        True if user has at least one of the roles, False otherwise.
    """
    user_roles = set(get_current_user_roles())
    required_roles = set(role_names)
    return bool(user_roles.intersection(required_roles))


def is_admin_secretaria() -> bool:
    """Check if current user has admin_secretaria role.

    Returns:
        True if user is admin_secretaria, False otherwise.
    """
    return has_role("admin_secretaria")


def is_admin_escola() -> bool:
    """Check if current user has admin_escola role.

    Returns:
        True if user is admin_escola, False otherwise.
    """
    return has_role("admin_escola")


def is_any_admin() -> bool:
    """Check if current user has any admin role.

    Returns:
        True if user is admin_secretaria or admin_escola, False otherwise.
    """
    return is_admin_secretaria() or is_admin_escola()
