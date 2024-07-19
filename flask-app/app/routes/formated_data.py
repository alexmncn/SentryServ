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
    try:
        devices_data = data.devices_connection_data()
        if devices_data:
            response = jsonify(devices_data)
            code = 200
        else:
            response = jsonify({'error': 'Devices data not found'})
            code = 404
    except Exception as e:
        response = jsonify({'error': 'An internal error occurred'})
        code = 500
        print(f'Error al obtener datos de la conexión de los dispositivos ==> {e}')
        
    return response, code
   

@formated_data_bp.route('/sensors/last-entry', methods=['GET'])
def last_sensor_entry():
    sensor = int(request.args.get('sensor', 1))
    try:
        sensor_data = data.last_sensor_entry(sensor)
        if sensor_data:
            response = jsonify(sensor_data)
            code = 200
        else:
            response = jsonify({'error': 'Sensor data not found'})
            code = 404
    except Exception as e:
        response = jsonify({'error': 'An internal error occurred'})
        code = 500
        print(f'Error al importar datos de los sensores ==> {e}')
        
    return response, code


@formated_data_bp.route('/sensors/chart-data', methods=['GET'])
def sensors_chart_data():
    sensor = request.args.get('sensor', '1')
    time = request.args.get('time', '24h')
    samples = int(request.args.get('samples', '24'))
    return jsonify(data.sensors_chart(sensor, time, samples))


@formated_data_bp.route('/mqtt-service/status', methods=['GET'])
@formated_data_bp.route('/mqtt-service/status/<option>', methods=['GET'])
def mqtt_service_control(option=None):
    try:
        if option:
            mqtt_service_data = sensors.mqtt_app_control('change_status', option)
            if mqtt_service_data['action'] == 'success':
                response = jsonify(action=mqtt_service_data['action'], status=mqtt_service_data['status'])
                code = mqtt_service_data['code']
            else:
                response = jsonify(action=mqtt_service_data['action'], error=mqtt_service_data['error'])
                code = mqtt_service_data['code']
        else:
            return jsonify(data.mqtt_app_control('status'))
    except Exception as e:
        response = jsonify({'error': 'An internal error occurred'})
        code = 500
        print(f'Error al importar datos de los sensores ==> {e}')
    
    return response, code
        

@formated_data_bp.route('/last-access-log-entry', methods=['GET'])
@formated_data_bp.route('/last-access-log-entry/<int:limit>', methods=['GET'])
def last_access_log_query(limit=10):
    ip_filter =''
    try:
        ip_filter = load_temporal_user_ip(current_user.id)
    except:
        ip_filter = None
        
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
