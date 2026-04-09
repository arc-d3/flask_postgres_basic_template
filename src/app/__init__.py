import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from flask_jwt_extended import JWTManager

jwt = JWTManager()

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(testing_config=None):

    app = Flask(__name__, template_folder="./templates")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "test_secret_key")
    
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev_jwt_key")
    jwt.init_app(app)

    # for test mode
    if testing_config:
        app.config.update(testing_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            f"postgresql://{os.environ.get("POSTGRES_USER", "test_user")}"
            f":{os.environ.get("POSTGRES_PASSWORD", "test_password")}"
            f"@db:5432/{os.environ.get("POSTGRES_DB", "test_db")}"
        )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"


    from .models.user import User
    from .models.api_key import ApiKey

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes import register_bp
    register_bp(app)
    
    # if there is no users initialize one
    from sqlalchemy import inspect as sa_inspect
    with app.app_context():
        if sa_inspect(db.engine).has_table("users"):
            if db.session.execute(db.select(User)).first() is None:
                user = User()
                user.name = "SUPERADMIN"
                user.email = os.getenv("INITIAL_SUPERADMIN_EMAIL", "test@gmail.com")
                user.set_password(os.getenv("INITIAL_SUPERADMIN_PASSWORD", "test123"))

                db.session.add(user)
                db.session.commit()

    return app