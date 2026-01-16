from main import create_app
from src.config.db_config import db
from src.models.role import Role


def seed_roles():
    """Create initial roles in the database if they don't exist.

    This function creates the following roles:
    - admin_secretaria: Can access all schools (super admin)
    - admin_escola: Can only access their own school (school admin)

    The function checks if roles already exist before creating them to avoid duplicates.
    """
    app = create_app()

    with app.app_context():
        admin_secretaria = (
            db.session.query(Role).filter(Role.name == "admin_secretaria").first()
        )
        if not admin_secretaria:
            admin_secretaria = Role(name="admin_secretaria")  # pyright: ignore[reportCallIssue]
            db.session.add(admin_secretaria)
            print("✓ Role 'admin_secretaria' criada")
        else:
            print("ℹ Role 'admin_secretaria' já existe")

        admin_escola = (
            db.session.query(Role).filter(Role.name == "admin_escola").first()
        )
        if not admin_escola:
            admin_escola = Role(name="admin_escola")  # pyright: ignore[reportCallIssue]
            db.session.add(admin_escola)
            print("✓ Role 'admin_escola' criada")
        else:
            print("ℹ Role 'admin_escola' já existe")

        db.session.commit()
        print("\n✓ Seeds executados com sucesso")


if __name__ == "__main__":
    seed_roles()
