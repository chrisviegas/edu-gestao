from flask import Flask
from flask_migrate import Migrate
from src.models.config.db_config import init_db, db

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    init_db(app)
    
    migrate.init_app(app=app, db=db)
    
    return app