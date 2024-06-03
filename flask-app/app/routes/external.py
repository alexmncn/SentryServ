"""External views."""
from flask import Blueprint, redirect 
from flask_login import login_required, current_user

from app.services.user import user_has_role
from app.services.pushover_notifications import send_noti

external_bp = Blueprint('external', __name__)


@external_bp.route('/get-adminer')
@user_has_role('admin')
def redirigir_a_adminer():
    message = f"{current_user.username} ha accedido a Adminer."
    send_noti(message, current_user.username)
    return redirect('/adminer/adminer-4.8.1.php')


@external_bp.route('/get-practicas')
def redirect_practicas():
    return redirect('/practicas')


@external_bp.route('/get-movie-web')
def redirect_movie_web():
    message = f"{current_user.username} ha accedido a Movie-Web"
    send_noti(message, current_user.username)
    return redirect('/movie-web')
