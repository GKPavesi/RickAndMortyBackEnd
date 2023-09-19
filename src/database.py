from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime

db = SQLAlchemy()
ma = Marshmallow()

class Characters(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False)
    status = db.Column(db.String(50), nullable = False)
    species = db.Column(db.String(100), nullable = False)
    type = db.Column(db.String(100), nullable = True)
    gender = db.Column(db.String(50), nullable = False)
    origin_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    current_id = db.Column(db.Integer, db.ForeignKey('locations.id'), nullable=True)
    image = db.Column(db.String(100), nullable = False)

    origin_location = db.relationship('Locations', foreign_keys=[origin_id], backref='origin_characters')
    current_location = db.relationship('Locations', foreign_keys=[current_id], backref='current_characters')
    episodes = db.relationship('Episodes', secondary='episodes_characters')

    @hybrid_property
    def most_recent_episode(self):
        if self.episodes:
            return max(self.episodes, key=lambda episode: episode.id)   

class Locations(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False)
    type = db.Column(db.String(100), nullable = False)
    dimension = db.Column(db.String(100), nullable = False)

    @property
    def residents_count(self):
        return len(self.current_characters)


class Episodes(db.Model):
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    name = db.Column(db.String(200), nullable = False)
    air_date = db.Column(db.String(100), nullable = False)
    episode = db.Column(db.String(150), nullable = False)

class Episodes_characters(db.Model):
    episode_id = db.Column(db.Integer, db.ForeignKey('episodes.id'), primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), primary_key=True)

class LocationsSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type', 'dimension', 'residents_count')

class EpisodeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'air_date', 'episode')

class CharactersSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'species', 'image', 'status') 

characters_schema = CharactersSchema(many=True)

class CharacterSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'status', 'species', 'type', 'gender', 'image', 'origin_location', 'current_location', 'most_recent_episode')
    
    origin_location = ma.Nested(LocationsSchema)
    current_location = ma.Nested(LocationsSchema)       
    most_recent_episode = ma.Nested(EpisodeSchema)       

character_schema = CharacterSchema()


class ExceptionTracker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    error_message = db.Column(db.Text, nullable=True)
    request_headers = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    endpoint = db.Column(db.String(500), nullable=True)
    http_method = db.Column(db.String(10), nullable=True)
    traceback = db.Column(db.Text, nullable=True)

class SearchLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    request_headers = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)
    endpoint = db.Column(db.String(255), nullable=True)
    success = db.Column(db.Boolean, nullable = False)
    search_result_cached = db.Column(db.Boolean, nullable = False)
    status_code = db.Column(db.Integer, nullable = False)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firebase_uid = db.Column(db.String(200), nullable = False, unique = True)
    first_name = db.Column(db.String(125), nullable = False)
    last_name = db.Column(db.String(125), nullable = False)
    email = db.Column(db.String(200), nullable = False, unique = True)

class UserSchema(ma.Schema):
    firebase_uid = ma.String(required=True)
    first_name = ma.String(required=True)
    last_name = ma.String(required=True)
    email = ma.String(required=True)

user_schema = UserSchema()
