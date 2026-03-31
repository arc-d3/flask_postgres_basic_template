from app.services.auth_service import register_user, authenticate_user

def test_register_user(app):
    assert register_user(
        name="test",
        email="b@b.com",
        password="qwerty"
    ) is True


# test duplicate


def test_authenticate_user(app):
    register_user(
        name="test",
        email="b@b.com",
        password="qwerty"
    )

    assert authenticate_user(
        email="b@b.com",
        password="qwerty"
    ) is not None

# Test wrong password