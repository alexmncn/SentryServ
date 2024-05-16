"""Data functions."""

from flask_login import current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_
import re

from app.services.access_log_db import access_log_table, query as access_log_query
from app.services.system import get_cpu_usage, get_ram_usage, get_cpu_temp
from app.services.net_and_connections import check_device_connection, pc_status, net_detect, scan_network
from app.services.sensors import sensor_data_db, mqtt_app_control
from app.services.user import load_credentials
from app.models import StaticDevices

# PENDING DICTIONARY FORMAT - Also the JS

def load_user_credentials():
    session_user_id = current_user.id

    user_credentials = load_credentials(session_user_id)

    user_credentials_dc = [
        {
            "id": credentials.id, 
            "user_id": credentials.user_id, 
            "site": credentials.site, 
            "user": credentials.user, 
            "email": credentials.email,
            "password": credentials.password,
            "description": credentials.description
        } 
        for credentials in user_credentials
    ]

    return user_credentials_dc


def scan_local_devices():
    ip_range = f'192.168.{net_detect()}.0/24'
    result = scan_network(ip_range)

    hosts_data = []

    if result.returncode == 0:
        # Extract IPs and hostnames using regular names
        pattern = re.compile(r'Nmap scan report for (.+) \((\d+\.\d+\.\d+\.\d+)\)')
        matches = pattern.findall(result.stdout)

        for i, match in enumerate(matches, start=1):
            host_name, ip = match
            hosts_data.append({'Host': host_name, 'IP': ip, 'Status':'Activo'})
    else:
        print(f'Error: {result.stderr}')
    return hosts_data


#obtener_datos_json_tablas
def devices_connection_data():
    static_devices = StaticDevices.query.all()
    
    devices_status = []

    for device in static_devices:
        status = check_device_connection(device.ip)
        
        devices_status.append({'name': device.name, 'IP': device.ip, 'status': status})

    return devices_status


# Obtener datos tabla 3 raspberry server
def server_info():
    temp = get_cpu_temp()
    rsp_temp = f'{temp} ºC'

    cpu = round(float(get_cpu_usage()), 1)
    cpu_usage = f'{cpu} %'

    ram = get_ram_usage()
    ram_usage = f'{ram} MB'


    server_info = {
        'temp': {'status-data': rsp_temp},
        'cpu-usage':{'status-data': cpu_usage},
        'ram-usage':{'status-data': ram_usage},
    }

    return server_info


def pc_status_info():
    pc_status_ = pc_status()
    #send_notis.send_noti(pc_stats, 'default')

    status = {
        'pc-status': {'status-data': pc_status_},
    }
    
    return status


def last_sensor_entry(limit=1):
    status_json = None
    try:
        s_name, temp, humd, date, battery = sensor_data_db(limit)

        temp = f'{temp} ºC'
        humd = f'{humd} %'
        battery = f'{round(float(battery), 1)} %'

        status_json = {
            'sensor_name':{'status-data': s_name},
            'temperature':{'status-data': temp},
            'humidity':{'status-data': humd},
            'battery':{'status-data': battery},
            'date':{'status-data': date}
        }
    except:
        print('Error')
    
    return status_json or None


def mqtt_app_status():
    status = 'error'
    since_date = 'error'

    status, since_date, since_time = mqtt_app_control('status')

    status_json = {
        'status': status,
        'date': since_date,
        'time': since_time
    }

    return status_json


def last_access_log_query(limit=10, ip_filter=None, user_login=False, additonal_columns=None):
    #parametros query
    selects = None
    
    columns = ['id', 'remote_host', 'date']

    if additonal_columns:
        for column in additonal_columns:
            columns.append(column)
    
    if ip_filter:
        filter = access_log_table.columns.remote_host != f'{ip_filter}'
    elif user_login is True:
        filter1 = access_log_table.columns.request_method = 'POST'
        filter2 = access_log_table.columns.request_uri = '/login/'
        filter = and_(filter1, filter2)
    else:
        filter = None
    
    order = access_log_table.columns.id.desc()


    resultados = access_log_query(selects=selects, columns=columns, filters=filter, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list


def most_accesses_by_ip_query(limit=10):
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    #parametros query
    selects = [access_log_table.c.remote_host,func.count().label('count'),func.max(access_log_table.c.date).label('last_access')]
    columns = None
    filters = access_log_table.c.date >= time_threshold
    group = access_log_table.c.remote_host
    order = func.count().desc()
    
    resultados = access_log_query(selects=selects, columns=columns, filters=filters, group_by=group, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list
