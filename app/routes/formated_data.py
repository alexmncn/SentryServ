"""Formated data routes. Return data for js Ajax request for the web visualization."""
from flask import Blueprint, jsonify

from app.services import data

formated_data_bp = Blueprint('formated_data', __name__)


@formated_data_bp.route('/server-info', methods=['GET'])
def server_info():
    return jsonify(data.server_info())

@formated_data_bp.route('/pc-status', methods=['GET'])
def pc_status():
    return jsonify(data.pc_status_info())

@formated_data_bp.route('/devices-connection_status', methods=['GET'])
def devices_connection_status():
    return jsonify(data.devices_connection_status())

@formated_data_bp.route('/last_sensor_entry', methods=['GET'])
def last_sensor_entry():
    return jsonify(data.last_sensor_entry())
