import logging

logger = logging.getLogger(__name__)

from app import db
from app.models.api_key import ApiKey
import hashlib
import secrets

def create_api_key(user_id: int, name: str) -> str|None:
    
    try:
        raw_key = secrets.token_hex(32)
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()

        api_key = ApiKey()
        api_key.name = name
        api_key.key_hash = key_hash
        api_key.owner_id = user_id

        db.session.add(api_key)
        db.session.commit()

        logger.info("Successfully created API Key for user %s", user_id)
        return raw_key
    except Exception as e:
        logger.error("failed to create API Key ofr user %s: %s", user_id, e)
        db.session.rollback()
        return None

def get_all_api_keys(user_id: int) -> list :
    try:
        keys = db.session.execute(db.select(ApiKey).filter_by(owner_id=user_id)).scalars().all()

        return keys
    except Exception as e:
        logger.error("Error getting api key for %s: %s", user_id, e)

        return []