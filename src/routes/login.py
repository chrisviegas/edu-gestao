from flask import Blueprint, request, jsonify
from src.repositories.user_repository import UserRepository
from src.services.auth_service import generate_token
from src.utils.password_utils import verify_password

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("", methods=["POST"])
def login():
    """Authenticate user and return JWT token.

    Expected JSON body:
        {
            "email": str,
            "password": str
        }

    Returns:
        200: Login successful with JWT token, user info, roles, and school_id
        400: Missing email or password in request
        401: Invalid credentials (user not found or wrong password)
        403: User has no role assigned
    """
    data = request.get_json()

    if not data or "email" not in data or "password" not in data:
        return jsonify(msg="Email e senha são obrigatórios"), 400

    email = data.get("email")
    password = data.get("password")

    user = UserRepository.find_by_email(email)

    if not user:
        return jsonify(msg="Credenciais inválidas"), 401

    if not verify_password(password, user.hash_password):
        return jsonify(msg="Credenciais inválidas"), 401

    if not user.roles:
        return jsonify(msg="Usuário não possui role atribuída"), 403

    token = generate_token(user)

    return jsonify(
        {
            "access_token": token,
            "user": user.to_dict(),
            "roles": [role.name for role in user.roles],
            "school_id": user.school_id,
        }
    ), 200
