from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

db = SQLAlchemy()

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['SECRET_KEY']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hjqfofumhrnhjm:ea725535755803f36ade040fb1bdefb7ba111c10ab7a963ca2832d1944a7fe55@ec2-18-210-191-5.compute-1.amazonaws.com:5432/de86b6vsn43178'
    uri = os.getenv("DATABASE_URL")
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # blueprint for auth routes in the app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non auth routes in the app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
