import pytest

from app import create_app, db 

@pytest.fixture()
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

# fixture , simulate web but not login
@pytest.fixture()
def client(app):

    return app.test_client()

#  simulate web and login
@pytest.fixture()
def logged_in_client(app):
    from app.services.auth_service import register_user

    with app.app_context():
        register_user(
            name="testuser",
            email="testemail@gmail.com",
            password="testpassword"
        )
    
    client = app.test_client()
    response = client.post("/login", data={
        "email":"testemail@gmail.com",
        "password":"testpassword"
    })

    return client

# no broswer simulation but user exist
@pytest.fixture()
def registered_user(app):
    from app.services.auth_service import register_user
    from app.models.user import User

    with app.app_context():
        register_user(
            name="testuser",
            email="testuser@gmail.com",
            password="testpassword"
        )

        user = db.session.execute(db.select(User).filter_by(email="testuser@gmail.com")).scalar_one()

        return user.id