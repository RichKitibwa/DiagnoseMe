from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from flask_migrate import Migrate

db = SQLAlchemy()

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ['SECRET_KEY']
    app.config['UPLOAD_FOLDER'] = 'static/uploads'
    # allowed_extensions = {'txt', 'pdf', 'jpg', 'jpeg'}
    #
    # def allowed_files(filename):
    #     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_DATABASE_URI'] ='postgresql://yoyudupkzhogzu:16fc30e8e4c3d68985df1b8e84954730994f9a18aaee4859ac003542d5073e8e@ec2-52-54-212-232.compute-1.amazonaws.com:5432/dbfeqkhbjted3d'
    app.config['SQLALCHEMY_DATABASE_URI'] =os.environ['DATABASE_URI']

    # uri = os.getenv("DATABASE_URL")
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    db.init_app(app)
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    migrate = Migrate(app, db)

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
