from flask import Blueprint, request, jsonify
from src.repositories.user_repository import UserRepository
from src.utils.password_utils import hash_password
from src.utils.decorators import any_admin, admin_secretaria_only
from src.services.auth_service import get_current_user_school_id, is_admin_secretaria

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/register", methods=["POST"])
def register():
    """Register a new user.

    Expected JSON body:
        {
            "name": str,
            "email": str,
            "password": str,
            "school_id": int,
            "role": str (optional, defaults to "admin_escola")
        }

    Returns:
        201: User created successfully with user data
        400: Invalid data or missing required fields
        409: Email already registered
    """
    data = request.get_json()

    if not data:
        return jsonify(msg="Dados inválidos"), 400

    required_fields = ["name", "email", "password", "school_id"]
    for field in required_fields:
        if field not in data:
            return jsonify(msg=f"Campo '{field}' é obrigatório"), 400

    email = data.get("email")

    if UserRepository.find_by_email(email):
        return jsonify(msg="Email já cadastrado"), 409

    hashed_password = hash_password(data.get("password"))

    user = UserRepository.create_user(
        name=data.get("name"),
        email=email,
        hashed_password=hashed_password,
        school_id=data.get("school_id"),
    )

    role_name = data.get("role", "admin_escola")

    UserRepository.add_role_to_user(user.id, role_name)

    return jsonify({"msg": "Usuário criado com sucesso", "user": user.to_dict()}), 201


@users_bp.route("", methods=["GET"])
@any_admin
def list_users():
    """List all users, filtered by role permissions.

    - admin_secretaria: Can see all users across all schools
    - admin_escola: Can only see users from their own school

    Returns:
        200: List of users with their roles and school_id
    """
    users = UserRepository.get_all_users()

    result = []
    for user in users:
        user_data = user.to_dict()
        user_data["roles"] = [role.name for role in user.roles]
        user_data["school_id"] = user.school_id
        result.append(user_data)

    if is_admin_secretaria():
        return jsonify({"users": result}), 200

    user_school_id = get_current_user_school_id()
    filtered_users = [u for u in result if u["school_id"] == user_school_id]

    return jsonify({"users": filtered_users}), 200


@users_bp.route("/<int:user_id>/role", methods=["PUT"])
@admin_secretaria_only
def update_user_role(user_id):
    """Update a user's role.

    Only accessible to admin_secretaria.

    Expected JSON body:
        {
            "role": str
        }

    Args:
        user_id: ID of user to update

    Returns:
        200: Role updated successfully
        400: Missing role field
        403: User not admin_secretaria
        404: User or role not found
    """
    data = request.get_json()

    if not data or "role" not in data:
        return jsonify(msg="Campo 'role' é obrigatório"), 400

    role_name = data.get("role")

    if UserRepository.add_role_to_user(user_id, role_name):
        return jsonify(msg="Role atualizada com sucesso"), 200

    return jsonify(msg="Usuário ou role não encontrado"), 404


@users_bp.route("/<int:user_id>", methods=["GET"])
@any_admin
def get_user(user_id):
    """Get details of a specific user.

    - admin_secretaria: Can access any user
    - admin_escola: Can only access users from their own school

    Args:
        user_id: ID of user to retrieve

    Returns:
        200: User details including roles and school_id
        403: Access denied (admin_escola trying to access different school)
        404: User not found
    """
    user = UserRepository.find_by_id(user_id)

    if not user:
        return jsonify(msg="Usuário não encontrado"), 404

    if not is_admin_secretaria():
        user_school_id = get_current_user_school_id()
        if user.school_id != user_school_id:
            return jsonify(msg="Acesso negado"), 403

    user_data = user.to_dict()
    user_data["roles"] = [role.name for role in user.roles]
    user_data["school_id"] = user.school_id

    return jsonify({"user": user_data}), 200
