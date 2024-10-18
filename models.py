from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timezone

db = SQLAlchemy()

# Association table

user_groups = db.Table('user_groups',
                       db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                       db.Column('group_id', db.Integer, db.ForeignKey('groups.id'), primary_key=True)
                       )

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    serialize_rules = ('-posts.user', '-groups.users',)
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(225))
    password = db.Column(db.String(50))
    
    posts = db.relationship('Post', back_populates="user")
    groups = db.relationship('Group', secondary=user_groups, back_populates="users")
    
    @validates('email')
    def validate_email(self, key, value):
        if '@' not in value:
            raise ValueError('@ must be a valid email address')
        return value
    
    def set_password(self, password):
        self.password = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    @classmethod
    def get_user_by_username(cls, username):
        return  cls.query.filter_by(username=username).first()
    
class Post(db.Model, SerializerMixin):
    __tablename__ = 'posts'
    
    serialize_rules = ('-user',)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    user = db.relationship("User", back_populates='posts')
    
class Group(db.Model, SerializerMixin):
    __tablename__ = "groups"
    
    id  =  db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    users = db.relationship('User', secondary=user_groups, back_populates="groups")
    
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(255), nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
