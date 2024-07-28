"""User related services."""
from flask import redirect, url_for, flash
from flask_login import login_user, current_user
from sqlalchemy import desc
from functools import wraps
import json

from app.extensions import db
from app.services.access_log_db import last_access_log_query
from app.services.pushover_notifications import send_noti
from app.models import Credentials, User, UsersLoginLog


def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        login_user(user) # Deprecated, soon removed
            
        # Save login log
        save_user_login_log(current_user.id)

        # Send notification
        message = f"{username} ha iniciado sesión en la web."
        send_noti(message, current_user.username)
        
        return True  
    return False


def register_new(username, password):
    # Check if a user with the same username existing_user
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return 409

    # Creates the new user instance and set password
    new_user = User(username=username)
    new_user.set_password(password)

    # Add new user to database
    db.session.add(new_user)
    db.session.commit()
    
    return 200


def user_has_role(role, redirect_=True, route=None):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return fn(*args, **kwargs)
            else:
                flash("No tienes permiso para acceder a esta página.", "danger")
                if redirect_:
                    if route:
                        return redirect(url_for(route))
                    return redirect(url_for('home.home'))
                return None
        return decorated_view
    return wrapper


def save_user_login_log(user_id):
    # Obtener el último acceso desde la base de datos
    last_login_access = last_access_log_query(limit=1, user_login=True)

    # Verificar si hay resultados
    if last_login_access:
        ip_temp = last_login_access[0]['remote_host']
        date = last_login_access[0]['date']

        last_user_login = UsersLoginLog(user_id=user_id, ip=ip_temp, date=date)

        db.session.add(last_user_login)
        db.session.commit()


def load_temporal_user_ip(user_id):
    last_user_login = UsersLoginLog.query.filter_by(user_id=user_id).order_by(desc(UsersLoginLog.date)).first()
    return last_user_login.ip


def load_credentials(user_id): 
    return Credentials.query.join(User).filter(Credentials.user_id == user_id).order_by(Credentials.site).all()
