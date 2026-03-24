from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json

db = SQLAlchemy()

class ApiCache(db.Model):
    """SQLite cache for API responses"""
    __tablename__ = 'api_cache'

    id = db.Column(db.Integer, primary_key=True)
    cache_key = db.Column(db.String(512), unique=True, nullable=False, index=True)
    data = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def get_data(self):
        return json.loads(self.data)

    @staticmethod
    def set(key, value, ttl_seconds):
        from datetime import timedelta
        expires = datetime.utcnow() + timedelta(seconds=ttl_seconds)
        entry = ApiCache.query.filter_by(cache_key=key).first()
        if entry:
            entry.data = json.dumps(value)
            entry.expires_at = expires
        else:
            entry = ApiCache(cache_key=key, data=json.dumps(value), expires_at=expires)
            db.session.add(entry)
        db.session.commit()

    @staticmethod
    def get(key):
        entry = ApiCache.query.filter_by(cache_key=key).first()
        if entry and entry.expires_at > datetime.utcnow():
            return entry.get_data()
        return None

class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    favorite_teams = db.relationship('FavoriteTeam', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

class FavoriteTeam(db.Model):
    """Model for storing user's favorite teams"""
    __tablename__ = 'favorite_teams'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    team_id = db.Column(db.Integer, nullable=False)
    team_name = db.Column(db.String(120), nullable=False)
    team_logo = db.Column(db.String(500))
    added_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (db.UniqueConstraint('user_id', 'team_id', name='uq_user_team'),)
    
    def __repr__(self):
        return f'<FavoriteTeam {self.team_name}>'
