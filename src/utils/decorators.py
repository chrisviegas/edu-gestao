from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*required_roles):
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