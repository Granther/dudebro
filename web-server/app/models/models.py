import uuid
from flask_login import UserMixin

from app import db

def generate_uuid():
    return str(uuid.uuid4())

class Games(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    name = db.Column(db.String, unique=True, nullable=False)
    available  = db.Column(db.Boolean, unique=False, nullable=True, server_default=True)

    def __str__(self):
        return self.name

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    username = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    container_limit = db.Column(db.Integer, nullable=True, default=1)
    containers = db.relationship('Containers', backref='users', lazy=True)

class Containers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    uuid = db.Column(db.String, nullable=True, default=generate_uuid)
    subdomain = db.Column(db.String, unique=True, nullable=False)
    srv_id = db.Column(db.String, unique=True, nullable=False)
    domain = db.Column(db.String, unique=False, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False)
    rcon_port = db.Column(db.Integer, unique=True, nullable=False)
    priority = db.Column(db.Integer, unique=False, nullable=True)
    weight = db.Column(db.Integer, unique=False, nullable=True)
    priority = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String, unique=False, nullable=False)
    type = db.Column(db.String, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


