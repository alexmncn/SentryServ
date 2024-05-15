"""User related services."""
from flask import redirect, url_for, flash
from flask_login import current_user
from sqlalchemy import desc
from functools import wraps
import json

from app.extensions import db
from app.services.access_log_db import last_access_log_query
from app.models import Credentials, User, UsersLoginLog


def user_has_role(role):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if current_user.is_authenticated and current_user.role == role:
                return fn(*args, **kwargs)
            else:
                flash("No tienes permiso para acceder a esta página.", "danger")
                return redirect(url_for('home.home'))
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
