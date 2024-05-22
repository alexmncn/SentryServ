"""Formated data routes. Return data for js Ajax request for the web visualization."""
from flask import Blueprint, redirect, request, jsonify
from flask_login import login_required, current_user

from app.services import data, access_log_db, sensors
from app.services.user import load_temporal_user_ip

formated_data_bp = Blueprint('formated_data', __name__)


@formated_data_bp.route('/server-info', methods=['GET'])
def server_info():
    return jsonify(data.server_info())

@formated_data_bp.route('/pc/status', methods=['GET'])
def pc_status():
    return jsonify(data.pc_status_info())

@formated_data_bp.route('/devices-connection-status', methods=['GET'])
def devices_connection_status():
    return jsonify(data.devices_connection_data())

@formated_data_bp.route('/last-sensor-entry/<int:sensor>', methods=['GET'])
def last_sensor_entry(sensor):
    return jsonify(data.last_sensor_entry(sensor))

@formated_data_bp.route('/mqtt-service/status', methods=['GET'])
@formated_data_bp.route('/mqtt-service/status/<option>', methods=['GET'])
def mqtt_service_control(option=None):
    if option:
        return jsonify(sensors.mqtt_app_control('change_status', option))
        
    else:
        return jsonify(data.mqtt_app_status())

@formated_data_bp.route('/last-access-log-entry', methods=['GET'])
@formated_data_bp.route('/last-access-log-entry/<int:limit>', methods=['GET'])
def last_access_log_query(limit=10):
    ip_filter = load_temporal_user_ip(current_user.id)
    return jsonify(access_log_db.last_access_log_query(limit=limit, ip_filter=ip_filter))

@formated_data_bp.route('/most-accesses-by-ip-entry', methods=['GET'])
@formated_data_bp.route('/most-accesses-by-ip-entry/<int:limit>', methods=['GET'])
def most_accesses_by_ip_query(limit=10):
    return jsonify(access_log_db.most_accesses_by_ip_query(limit))

@formated_data_bp.route('/net-devices-scan', methods=['GET'])
def net_devices_scan():
    return jsonify(data.scan_local_devices())

@formated_data_bp.route('/user/data/credentials', methods=['GET'])
@login_required
def user_credentials():
    return jsonify(data.load_user_credentials())
