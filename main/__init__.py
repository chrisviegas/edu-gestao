from flask import Flask
from flask_migrate import Migrate
from src.config.db_config import init_db, db
import os
from dotenv import load_dotenv

load_dotenv()

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    init_db(app)
    
    migrate.init_app(app=app, db=db)
    
    return app