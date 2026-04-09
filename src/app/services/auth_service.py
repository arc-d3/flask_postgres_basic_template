import logging

logger = logging.getLogger(__name__)

from app import db
from app.models.user import User

def register_user(name: str, email: str, password: str) -> bool:

    try:
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

        if user:
            logger.warning("Email Taken")
            return False
        
        user = User()
        user.name = name
        user.email = email
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        logger.info("Register success")
        return True
    
    except Exception as e:
        logger.error("Error in registerting user %s: %s", name, e)
        db.session.rollback()
        return False

def authenticate_user(email: str, password: str) -> User|None:

    try:
        user = db.session.execute(db.select(User).filter_by(email=email)).scalar_one_or_none()

        if user and user.check_password(password):
            logger.info("User logged in")
            return user

        logger.warning("Error login for %s", email)
        return None
    except Exception as e:
        logger.error("Error in authenticate user %s: %s", email, e)
        db.session.rollback()
        return None