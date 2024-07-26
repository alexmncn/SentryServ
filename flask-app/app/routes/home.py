"""App views."""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity
from datetime import datetime, timedelta
import pytz


from app.extensions import db, jwt, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.services.user import authenticate, register_new
from app.services.pushover_notifications import send_noti

home_bp = Blueprint('home', __name__)

blacklist = set()


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


@login_manager.user_loader
def load_user(user_id):
    # Load user by ID.
    return User.query.get(user_id)


@home_bp.route('/login', methods=['POST'])
def login():
    # User login
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user_authenticated = authenticate(username, password)
    
    if user_authenticated:
        expires_delta = timedelta(days=1)
        expires_date = datetime.now(pytz.utc) + expires_delta
        access_token = create_access_token(identity={'username': username}, expires_delta=expires_delta)
        return jsonify(token=access_token, expires_at=expires_date.isoformat(), username=username), 200
    
    return jsonify(message='Invalid credentials'), 401


@home_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Logout.
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify(message='Logged out successfully'), 200


@home_bp.route('/auth')
@jwt_required()
def auth():
    user = get_jwt_identity()
    return jsonify(user), 200


@home_bp.route('/register', methods=['POST'])
def register():
    # Register new user.
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    status = register_new(username, password)
    
    if status == 200:
        return jsonify(message='Registered successfully'), 200
    elif status == 409:
        return jsonify(message='This user already exists'), 409