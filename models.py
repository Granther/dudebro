from db_factory import db
from flask_login import UserMixin
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    username = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    containers = db.relationship('Containers', backref='users', lazy=True)

class Containers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    uuid = db.Column(db.String, nullable=True, default=generate_uuid)
    subdomain = db.Column(db.String, unique=True, nullable=False)
    domain = db.Column(db.String, unique=False, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False)
    priority = db.Column(db.Integer, unique=False, nullable=True)
    weight = db.Column(db.Integer, unique=False, nullable=True)
    priority = db.Column(db.Integer, unique=False, nullable=True)
    name = db.Column(db.String, unique=False, nullable=False)
    type = db.Column(db.String, unique=False, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # properties = db.relationship("ServerProperties", uselist=False, backref='containers', cascade="all, delete-orphan")

# class ServerProperties(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
#     container_id = db.Column(db.Integer, db.ForeignKey('containers.id'), unique=True)
#     container = db.relationship("Containers", backref="server_properties")

    # allow_flight = db.Column(db.String, nullable=True, default="false")
    # allow_nether = db.Column(db.String, nullable=True, default="true")
    # difficulty = db.Column(db.String, nullable=True, default="normal")
    # enforce_whitelist = db.Column(db.String, nullable=True, default="false")
    # gamemode = db.Column(db.String, nullable=True, default="")
    # hardcore = db.Column(db.String, nullable=True, default="")
    # level_name = db.Column(db.String, nullable=True, default="")
    # level_seed = db.Column(db.String, nullable=True, default="")
    # level_type = db.Column(db.String, nullable=True, default="")
    # max_players = db.Column(db.String, nullable=True, default="")
    # motd = db.Column(db.String, nullable=True, default="")
    # pvp = db.Column(db.String, nullable=True, default="")
    # query_port = db.Column(db.String, nullable=True, default="")
    # rcon_password = db.Column(db.String, nullable=True, default="")
    # rcon_port = db.Column(db.String, nullable=True, default="")
    # server_port = db.Column(db.String, nullable=True, default="")
    # simulation_distance = db.Column(db.String, nullable=True, default="")
    # view_distance = db.Column(db.String, nullable=True, default="")
    # white_list = db.Column(db.String, nullable=True, default="")

