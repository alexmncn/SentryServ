"""App views."""
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from flask_jwt_extended import create_access_token, jwt_required, get_jwt, get_jwt_identity

from app.extensions import db, jwt, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.services.user import authenticate
from app.services.pushover_notifications import send_noti

home_bp = Blueprint('home', __name__)

blacklist = set()

@login_manager.user_loader
def load_user(user_id):
    # Load user by ID.
    return User.query.get(user_id)


@home_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    user_authenticated = authenticate(username, password)
    
    if user_authenticated:
        access_token = create_access_token(identity={'username': username})
        return jsonify({'token': access_token, 'username': username}), 200
    
    return jsonify({'message': 'Invalid credentials'}), 401


@home_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    # Logout.
    logout_user() # Deprecated, soon removed
    jti = get_jwt()['jti']
    blacklist.add(jti)
    return jsonify(msg="Logged out successfully"), 200


@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    return jwt_payload['jti'] in blacklist


@home_bp.route('/register/', methods=['GET', 'POST'])
def register():
    # Register new user.
    form = RegisterForm()

    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check if a user with the same username existing_user
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash ('El nombre de usuario ya está en uso.\nPor favor, elige otro.', 'danger')
            return redirect(url_for('home.register'))

        # Creates the new user instance and set password
        new_user = User(username=username)
        new_user.set_password(password)

        db.session.add(new_user)
        db.session.commit()

        flash('¡Te has registrado correctamente! Ahora puedes iniciar sesión.', 'success')
        
        # Send notifitacion
        message = f"{username} se ha registrado en la web."
        send_noti(message, username)
        return redirect(url_for('home.login'))

    return render_template('register.html', form=form)
