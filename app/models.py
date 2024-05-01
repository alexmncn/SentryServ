"""Database models"""
from datetime import datetime

from .extensions import db

from flask_login import UserMixin
from sqlalchemy import Column, Integer, String

# Users
class User(UserMixin,db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), default='user',nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


# Credentials
class Credentials(db.Model):
    __tablename__ = "credentials"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    site = db.Column(db.String(255), nullable=False)
    user = db.Column(db.String(50), nullable=True)
    email = db.Column(db.String(255), nullable=True)
    password = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


# Sensors
class SensorData(db.Model):
    __tablename__ = "sensor_data"
    id = db.Column(db.Integer, primary_key=True,)
    sensor_name = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    humidity = db.Column(db.Float)
    date = db.Column(db.DateTime, unique=True, default=datetime.now)
    battery_level = db.Column(db.Float)
