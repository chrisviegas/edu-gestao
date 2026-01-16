from typing import Optional

from src.config.db_config import db
from src.models.user import User


class UserRepository:
    @staticmethod
    def find_by_email(email: str) -> Optional[User]:
        """Find a user by their email address.

        Args:
            email: User's email address.

        Returns:
            User object if found, None otherwise.
        """
        return db.session.query(User).filter(User.email == email).first()

    @staticmethod
    def find_by_id(user_id: int) -> Optional[User]:
        """Find a user by their ID.

        Args:
            user_id: User's unique identifier.

        Returns:
            User object if found, None otherwise.
        """
        return db.session.query(User).filter(User.id == user_id).first()

    @staticmethod
    def create_user(
        name: str, email: str, hashed_password: str, school_id: int
    ) -> User:
        """Create a new user with the provided details.

        Args:
            name: User's full name.
            email: User's email address.
            hashed_password: Pre-hashed password.
            school_id: ID of the school the user belongs to.

        Returns:
            Created User object.
        """
        user = User(
            name=name,  # pyright: ignore[reportCallIssue]
            email=email,  # pyright: ignore[reportCallIssue]
            hash_password=hashed_password,  # pyright: ignore[reportCallIssue]
            school_id=school_id,  # pyright: ignore[reportCallIssue]
        )
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def add_role_to_user(user_id: int, role_name: str) -> bool:
        """Assign a role to a user.

        Args:
            user_id: User's unique identifier.
            role_name: Name of the role to assign (e.g., 'admin_secretaria', 'admin_escola').

        Returns:
            True if role was assigned successfully, False if user or role not found.
        """
        from src.models.role import Role

        user = db.session.query(User).filter(User.id == user_id).first()
        role = db.session.query(Role).filter(Role.name == role_name).first()

        if not user or not role:
            return False

        if role not in user.roles:
            user.roles.append(role)
            db.session.commit()
        return True

    @staticmethod
    def get_all_users():
        """Retrieve all users from the database.

        Returns:
            List of all User objects.
        """
        return db.session.query(User).all()
