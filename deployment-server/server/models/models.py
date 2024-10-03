import uuid
from server import db

class GameTypes(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    name = db.Column(db.String, unique=False, nullable=True)
    fields = db.Column(db.String, unique=False, nullable=False)

    def __str__(self):
        return self.name