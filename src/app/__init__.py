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

def create_app():
    app = Flask(__name__, template_folder="./templates")
    app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"postgresql://{os.environ['POSTGRES_USER']}"
        f":{os.environ['POSTGRES_PASSWORD']}"
        f"@db:5432/{os.environ['POSTGRES_DB']}"
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