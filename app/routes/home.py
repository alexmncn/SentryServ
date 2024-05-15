"""App views."""
from flask import Blueprint, request, render_template, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user

from app.extensions import db, login_manager
from app.forms import LoginForm, RegisterForm
from app.models import User
from app.services.user import save_user_login_log
from app.services.pushover_notifications import send_noti

home_bp = Blueprint('home', __name__)


@login_manager.user_loader
def load_user(user_id):
    # Load user by ID.
    return User.query.get(user_id)


@home_bp.route('/', methods=['GET'])
def home():
    # Home page.
    return render_template('index.html')

@home_bp.route('/login/', methods=['GET', 'POST'])
def login():
    # Login the user.
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            
            # Save login log
            save_user_login_log(current_user.id)

            # Send notification
            message = f"{username} ha iniciado sesión en la web."
            send_noti(message, current_user.username)
            
            flash('Has iniciado sesión', 'success')
            return redirect(url_for("home.home"))
        else:
            flash('Credenciales incorrectas.\nPor favor, inténtalo de nuevo.', 'error')

    return render_template('login.html', form=form)


@home_bp.route('/logout/')
@login_required
def logout():
    # Logout.
    logout_user()
    flash('Has cerrado sesión', 'info')
    return redirect(url_for('home.home'))


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
