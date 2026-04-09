def register_bp(app):
    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    from .main import main_bp
    app.register_blueprint(main_bp)

    from .api import api_bp
    app.register_blueprint(api_bp)