"""Data functions."""
from flask_login import current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_
from collections import defaultdict
import numpy as np
import re

from app.services.access_log_db import access_log_table, query as access_log_query
from app.services.system import get_cpu_usage, get_ram_usage, get_cpu_temp
from app.services.net_and_connections import static_devices_data_db, check_device_connection, pc_status, net_detect, scan_network
from app.services.sensors import sensor_data_db, sensor_chart_data_db
from app.services.user import load_credentials
from app.models import SensorData


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
    scan_data = scan_network(ip_range, arguments='-sn')

    host_data = []

    for host in scan_data.all_hosts():
        host_name = scan_data[host].hostname()
        ip = host
        status = scan_data[host].state()
        host_data.append({'host': host_name, 'ip': ip, 'status': status})
        
    return host_data


def devices_connection_data():
    static_devices_data = static_devices_data_db()
    
    devices_status = []

    if static_devices_data:
        for device in static_devices_data:
            status = check_device_connection(device.ip)
            
            devices_status.append({'name': device.name, 'ip': device.ip, 'status': status})

    return devices_status or None


def server_info():
    temp = get_cpu_temp()
    rsp_temp = f'{temp} ºC'

    cpu = round(float(get_cpu_usage()), 1)
    cpu_usage = f'{cpu} %'

    ram = get_ram_usage()
    ram_usage = f'{ram} MB'


    server_info = {
        'temp': rsp_temp,
        'cpu-usage': cpu_usage,
        'ram-usage': ram_usage,
    }

    return server_info


def pc_status_info():
    pc_status_ = pc_status()

    status = {
        'pc-status': pc_status_,
    }
    
    return status


def last_sensor_entry(sensor_id=1):
    sensor_data = None
    s_data = sensor_data_db(sensor_id)
    
    if s_data:
        temp = f'{s_data.temperature} ºC'
        humd = f'{s_data.humidity} %'
        battery = f'{round(float(s_data.battery_level), 1)} %'

        sensor_data = {
            'sensor_name': s_data.sensor_name,
            'temperature': temp,
            'humidity':humd,
            'battery': battery,
            'date': s_data.date
        }
    
    return sensor_data


def process_sensor_data(rows, interval, sample_size):
    data_by_hour = defaultdict(list)
    
    for row in rows:
        if interval.endswith('h') and sample_size > 24:
            key = row.date.replace(second=0, microsecond=0)
        elif interval.endswith('h'):
            key = row.date.replace(minute=0, second=0, microsecond=0)
        elif interval.endswith('d'):
            key = row.date.replace(minute=0, second=0, microsecond=0)
        else:
            key = row.date  # No grouping
        
        data_by_hour[key].append(row)
    
    processed_data = []
    for key, entries in data_by_hour.items():
        avg_temp = round(np.mean([entry.temperature for entry in entries]), 2)
        avg_humidity = round(np.mean([entry.humidity for entry in entries]), 2)
        avg_battery = round(np.mean([entry.battery_level for entry in entries]), 2)
        processed_data.append(SensorData(sensor_name='default', temperature=avg_temp, humidity=avg_humidity, battery_level=avg_battery, date=key))

    return sample_data(processed_data, sample_size)


def sample_data(data, sample_size):
    if len(data) <= sample_size:
        return data

    sampled_data = []
    step = len(data) // sample_size
    for i in range(0, len(data), step):
        sampled_data.append(data[i])
    return sampled_data


def sensors_chart(sensor, time, samples):
    data = sensor_chart_data_db(sensor, time)
    data = process_sensor_data(data, time, samples)

    
    date_format = '%d-%m-%Y %H:%M'
    time_h = time.endswith('h')
    time_d = time.endswith('d')
    time_n = int(time[:-1])  
    if time_h:
        if time_n <= 24:
            date_format = '%H:%M'
        else:
            date_format = '%d - %H:%M'
    elif time_d:
        if time_n <= 31:
            date_format = '%d - %H:%M'
        elif time_n <= 365:
            date_format = '%d-%m - %H:%M'


    categories = [record.date.strftime(date_format) for record in data]
    temperature_series = {
        'name': 'Temperature',
        'data': [record.temperature for record in data],
        'color': '#FF0000'
    }
    humidity_series = {
        'name': 'Humidity',
        'data': [record.humidity for record in data],
        'color': '#0000FF'
    }
    battery_series = {
        'name': 'Battery Level',
        'data': [record.battery_level for record in data],
        'color': '#00FF00'
    }

    chart_data = {
        'categories': categories,
        'series': [temperature_series, humidity_series, battery_series]
    }
    
    return chart_data


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
