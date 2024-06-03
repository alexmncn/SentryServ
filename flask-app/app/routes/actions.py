"""Server actions routes."""
from flask import Blueprint, redirect, url_for, flash
from flask_login import current_user

from app.services.net_and_connections import pc_on_esp32
from app.services.user import user_has_role
from app.services.sensors import mqtt_app_control 
from app.services.pushover_notifications import send_noti

from app.config import PC_ON_ROUTE 

actions_bp = Blueprint('actions', __name__)


##secured pc-on con esp32 // ACTIVA
@actions_bp.route('/pc/on', methods=['GET','POST'])
@user_has_role('admin')
def pc_on():
    result = pc_on_esp32()
    flash(result)

    message = f'{current_user.username} ha encendido el PC desde la web.'
    send_noti(message, current_user.username)

    return redirect(url_for('home.home'))

##unsecured_pc_on con esp32 // ACTIVA
@actions_bp.route(PC_ON_ROUTE, methods=['GET', 'POST'])
def unsecured_pc_on():
    result = pc_on_esp32()
    flash(result)
    
    if (result == 'El PC ya está encendido'):
        send_noti('Se ha intentado encender el PC, pero ya está encendido.', 'default')
    else:
        send_noti('Se ha encendido el PC remotamente', 'default')

    return redirect(url_for('home.home'))
