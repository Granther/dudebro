import uuid
from flask_login import UserMixin

from app import db

def generate_uuid():
    return str(uuid.uuid4())

class Games(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    name = db.Column(db.String, unique=True, nullable=False)
    available  = db.Column(db.Boolean, unique=False, nullable=True, default=True)
    game_type = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return self.game_type

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    username = db.Column(db.String, unique=False, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    game_server_limit = db.Column(db.Integer, nullable=True, default=1)
    
    game_servers = db.relationship('GameServers', backref='users', lazy=True)

class GameServers(db.Model):
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    game_server_config = db.relationship('GameServerConfigs', backref='game_servers', lazy='dynamic')

class GameServerConfigs(db.Model):
    __tablename__ = 'game_server_configs'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    custom_name = db.Column(db.String, unique=False, nullable=False)
    type = db.Column(db.String(50))
    
    game_server_id = db.Column(db.Integer(), db.ForeignKey('game_servers.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'game_server_configs',
        'with_polymorphic': '*',
        'polymorphic_on': type,
    }

# Config for container deployment, user can game config later in process
class MinecraftConfigs(GameServerConfigs):
    __tablename__ = 'minecraft_configs'
    id = db.Column(db.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created = db.Column(db.TIMESTAMP, nullable=False, server_default=db.func.now())
    subdomain = db.Column(db.String, unique=True, nullable=False)
    num_players = db.Column(db.Integer(), unique=False, nullable=True, default=10)
    version = db.Column(db.String(), unique=False, nullable=False)

    config_id = db.Column(db.Integer(), db.ForeignKey('game_server_configs.id'))

    __mapper_args__ = {
        'polymorphic_identity': 'minecraft_configs',
        'with_polymorphic': '*'
    }

    # srv_id = db.Column(db.String, unique=True, nullable=False)
    # domain = db.Column(db.String, unique=False, nullable=False)
    # port = db.Column(db.Integer, unique=True, nullable=False)
    # rcon_port = db.Column(db.Integer, unique=True, nullable=False)
    # priority = db.Column(db.Integer, unique=False, nullable=True)
    # weight = db.Column(db.Integer, unique=False, nullable=True)