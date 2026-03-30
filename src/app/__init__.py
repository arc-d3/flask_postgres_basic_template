import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from dotenv import load_dotenv
load_dotenv()

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(testing_config=None):

    app = Flask(__name__, template_folder="./templates")
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "test_secret_key")

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

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from .routes.auth import auth_bp
    app.register_blueprint(auth_bp)

    from .routes.main import main_bp
    app.register_blueprint(main_bp)
    
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