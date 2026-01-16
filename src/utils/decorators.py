from functools import wraps

from flask import jsonify, request
from flask_jwt_extended import get_jwt, verify_jwt_in_request


def roles_required(*required_roles):
    """Decorator to require specific roles to access a route.

    Args:
        *required_roles: One or more role names required for access.

    Returns:
        Decorator function that checks if user has at least one required role.

    Example:
        @roles_required("admin_secretaria", "admin_escola")
        def some_route():
            return jsonify(msg="Access granted")
    """

    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_roles = set(claims.get("roles", []))

            if user_roles.intersection(required_roles):
                return fn(*args, **kwargs)

            return jsonify(msg="Acesso negado"), 403

        return decorator

    return wrapper


def school_required(fn):
    """Decorator to enforce school-scoped access control.

    - admin_secretaria: Can access any school (bypass school check)
    - admin_escola: Can only access their own school

    The decorator checks for school_id in kwargs or URL parameters (e.g., /api/schools/<school_id>).

    Returns:
        Decorated function that enforces school-scoped access.

    Example:
        @school_required
        def get_school(school_id):
            return jsonify(data={})
    """

    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        user_roles = claims.get("roles", [])
        user_school_id = claims.get("school_id")

        if "admin_secretaria" in user_roles:
            return fn(*args, **kwargs)

        if "admin_escola" in user_roles:
            school_id = kwargs.get("school_id")
            if not school_id and request.view_args:
                school_id = request.view_args.get("school_id")

            if school_id and school_id != user_school_id:
                return jsonify(
                    msg="Acesso negado: você não tem permissão para acessar esta escola"
                ), 403

            return fn(*args, **kwargs)

        return jsonify(msg="Acesso negado"), 403

    return decorator


def admin_secretaria_only(fn):
    """Decorator to restrict access to admin_secretaria role only.

    Returns:
        Decorated function that only allows admin_secretaria access.

    Example:
        @admin_secretaria_only
        def admin_only_route():
            return jsonify(msg="Admin only")
    """

    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        if "admin_secretaria" in claims.get("roles", []):
            return fn(*args, **kwargs)

        return jsonify(msg="Acesso negado: requer permissão de admin_secretaria"), 403

    return decorator


def any_admin(fn):
    """Decorator to require any admin role (admin_secretaria or admin_escola).

    Returns:
        Decorated function that allows either admin role.

    Example:
        @any_admin
        def admin_route():
            return jsonify(msg="Admin access granted")
    """

    @wraps(fn)
    def decorator(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()

        user_roles = claims.get("roles", [])

        if "admin_secretaria" in user_roles or "admin_escola" in user_roles:
            return fn(*args, **kwargs)

        return jsonify(msg="Acesso negado"), 403

    return decorator
