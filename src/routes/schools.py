from flask import Blueprint, request, jsonify
from src.repositories.school_repository import SchoolRepository
from src.services.school_service import SchoolService
from src.utils.decorators import any_admin, admin_secretaria_only, school_required

schools_bp = Blueprint("schools", __name__, url_prefix="/api/schools")


@schools_bp.route("", methods=["POST"])
@any_admin
def create_school():
    """Create a new school.

    Expected JSON body:
        {
            "name": str,
            "address": {
                "street": str,
                "number": str,
                "neighborhood": str,
                "city": str,
                "state": str,
                "zip_code": str
            },
            "school_type": str (federal, estadual, municipal, privada)
        }

    Returns:
        201: School created successfully with school data
        400: Invalid data or missing required fields
        400: Invalid school_type
    """
    data = request.get_json()

    if not data:
        return jsonify(msg="Dados inválidos"), 400

    required_fields = ["name", "address", "school_type"]
    for field in required_fields:
        if field not in data:
            return jsonify(msg=f"Campo '{field}' é obrigatório"), 400

    address = data.get("address")
    if not isinstance(address, dict):
        return jsonify(msg="Campo 'address' deve ser um objeto"), 400

    result = SchoolService.create_school_with_address(
        name=data.get("name"), address=address, school_type=data.get("school_type")
    )

    if result is None:
        return jsonify(msg="Tipo de escola inválido"), 400

    return jsonify({"msg": "Escola criada com sucesso", "school": result}), 201


@schools_bp.route("", methods=["GET"])
@any_admin
def list_schools():
    """List schools with pagination, filtered by role permissions.

    Query parameters:
        page: Page number (default: 1)
        per_page: Items per page (default: 20, max: 100)
        include_deleted: Whether to include soft-deleted schools (true/false, default: false)

    Returns:
        200: Paginated list of schools
    """
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 20, type=int)
    include_deleted = request.args.get("include_deleted", "false").lower() == "true"

    result = SchoolService.get_accessible_schools(
        page=page, per_page=per_page, include_deleted=include_deleted
    )

    schools_data = [
        school.to_dict(include_deleted=include_deleted) for school in result["schools"]
    ]

    return jsonify({"schools": schools_data, "pagination": result["pagination"]}), 200


@schools_bp.route("/<int:school_id>", methods=["GET"])
@school_required
def get_school(school_id):
    """Get details of a specific school.

    Query parameters:
        include_deleted: Whether to include deleted_at field (true/false, default: false)

    Args:
        school_id: ID of school to retrieve

    Returns:
        200: School details
        403: Access denied
        404: School not found
    """
    include_deleted = request.args.get("include_deleted", "false").lower() == "true"
    school = SchoolRepository.find_by_id(school_id, include_deleted=include_deleted)

    if not school:
        return jsonify(msg="Escola não encontrada"), 404

    return jsonify({"school": school.to_dict(include_deleted=include_deleted)}), 200


@schools_bp.route("/<int:school_id>", methods=["PUT"])
@school_required
def update_school(school_id):
    """Update a school.

    Query parameters:
        include_deleted: Whether to include deleted_at field in response (true/false, default: false)

    Expected JSON body (all optional):
        {
            "name": str,
            "address": {
                "street": str,
                "number": str,
                "neighborhood": str,
                "city": str,
                "state": str,
                "zip_code": str
            },
            "school_type": str
        }

    Args:
        school_id: ID of school to update

    Returns:
        200: School updated successfully
        400: Invalid school_type
        403: Access denied
        404: School not found
    """
    data = request.get_json()

    if not data:
        return jsonify(msg="Dados inválidos"), 400

    include_deleted = request.args.get("include_deleted", "false").lower() == "true"

    # Validate address if provided
    address = data.get("address")
    if address is not None and not isinstance(address, dict):
        return jsonify(msg="Campo 'address' deve ser um objeto"), 400

    result = SchoolService.update_school_with_address(
        school_id=school_id,
        name=data.get("name"),
        address=address,
        school_type=data.get("school_type"),
    )

    if result is None:
        return jsonify(msg="Escola não encontrada ou tipo inválido"), 404

    return jsonify({"msg": "Escola atualizada com sucesso", "school": result}), 200


@schools_bp.route("/<int:school_id>", methods=["DELETE"])
@admin_secretaria_only
def delete_school(school_id):
    """Soft delete a school.

    Only accessible to admin_secretaria.

    Args:
        school_id: ID of school to delete

    Returns:
        200: School deleted successfully
        403: Access denied (not admin_secretaria)
        404: School not found or already deleted
    """
    success = SchoolRepository.soft_delete_school(school_id)

    if not success:
        return jsonify(msg="Escola não encontrada"), 404

    return jsonify(msg="Escola excluída com sucesso"), 200


@schools_bp.route("/<int:school_id>/restore", methods=["POST"])
@admin_secretaria_only
def restore_school(school_id):
    """Restore a soft-deleted school.

    Only accessible to admin_secretaria.

    Args:
        school_id: ID of school to restore

    Returns:
        200: School restored successfully
        403: Access denied (not admin_secretaria)
        404: School not found or not deleted
    """
    success = SchoolService.restore_school(school_id)

    if not success:
        return jsonify(msg="Escola não encontrada ou não foi excluída"), 404

    return jsonify(msg="Escola restaurada com sucesso"), 200
