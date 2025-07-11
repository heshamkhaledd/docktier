from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import json
import sys

db = SQLAlchemy()
login_manager = LoginManager()

def read_db_info():
    try:
        with open('app/db_info.json', 'r') as file:
            db_info = json.load(file)
            return db_info
    except FileNotFoundError:
        print("**Error: db_info.json not found, exiting...")
        sys.exit(1)
    except Exception as e:
        print(f"**Error reading db_info.json: {e}, exiting...")
        sys.exit(1)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dev'
    db_info = read_db_info()
    app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{db_info['user']}:{db_info['password']}@{db_info['host']}:{db_info['port']}/{db_info['db_name']}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    from .models import User
    from .auth import auth_bp
    from .routes import main_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)

    return app
