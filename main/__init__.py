import os

from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

from src.config.db_config import db, init_db

load_dotenv()

migrate = Migrate()
jwt = JWTManager()


def create_app():
    """Create and configure the Flask application.

    This function initializes:
    - Flask app instance
    - Database connection
    - JWT authentication
    - Flask-Migrate for database migrations
    - Route blueprints (login, users)

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    init_db(app)

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-jwt-secret-key")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False

    migrate.init_app(app=app, db=db)
    jwt.init_app(app)
    from src import models  # noqa: F401
    from src.routes.login import login_bp
    from src.routes.users import users_bp
    from src.routes.schools import schools_bp

    app.register_blueprint(login_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(schools_bp)

    return app
