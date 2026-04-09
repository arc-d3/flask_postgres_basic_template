from app import db
import datetime

class ApiKey(db.Model):
    __tablename__ = "api_keys"

    name = db.Column(db.String(25), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    key_hash = db.Column(db.String(256), nullable=False, unique=True)
    date_created = db.Column(db.DateTime(), default=lambda: datetime.datetime.now(datetime.timezone.utc))
    owner_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)