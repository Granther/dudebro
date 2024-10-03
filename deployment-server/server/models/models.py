import uuid

from server import db

# from sqlalchemy.dialects.postgresql import UUID

class GameTypes(db.Model):
    id = db.Column(db.dialects.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    name = db.Column(db.String, unique=False, nullable=True)
     = db.Column(db.String, unique=False, nullable=True)