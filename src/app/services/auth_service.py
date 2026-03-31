from app import db
from app.models.user import User

def register_user(name: str, email: str, password: str) -> bool:

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

    if user:
        print("Email Taken")
        return False
    
    user = User()
    user.name = name
    user.email = email
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    print("Register success")
    return True

def authenticate_user(email: str, password: str) -> User|None :

    user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

    if user and user.check_password(password):
        print("User logged in")
        return user
    
    print("Error login")
    return None