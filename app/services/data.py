"""Data functions."""
from datetime import datetime
from sqlalchemy import func

from app.services.access_log_db import access_log_table
from app.services.system import get_cpu_usage, get_ram_usage, get_cpu_temp
from app.services.sensors import sensor_data_db



#obtener_datos_json_tablas
def datos_status_tabla1():
    status_miquel = check_status.miquel()
    status_noe = check_status.noe()
    status_iphone = check_status.iphone()

    status_json = {
        'miquel': {'columnaSTATUS': status_miquel},
        'noe': {'columnaSTATUS': status_noe},
        'iphone': {'columnaSTATUS': status_iphone},
    }

    return status_json


#obtener datos tabla 3 raspberry server
def datos_status_tabla3():
    temp = get_cpu_temp()
    rsp_temp = f'{temp} ºC'

    cpu = round(float(get_cpu_usage()), 1)
    cpu_usage = f'{cpu} %'

    ram = get_ram_usage()
    ram_usage = f'{ram} MB'


    status_json = {
        'temp': {'status-data': rsp_temp},
        'cpu-usage':{'status-data': cpu_usage},
        'ram-usage':{'status-data': ram_usage},
    }

    return status_json


def datos_status_tabla4():
    pc_status_ = pc_status()
    #send_notis.send_noti(pc_stats, 'default')

    status_json = {
        'pc-status': {'status-data': pc_status_},
    }
    
    return status_json


def datos_status_tabla5():
    s_name, temp, humd, date, battery = sensor_data_db()

    temp = f'{temp} ºC'
    humd = f'{humd} %'

    status_json = {
        'sensor_name':{'status-data': s_name},
        'temperature':{'status-data': temp},
        'humidity':{'status-data': humd},
        'date':{'status-data': date},
        'battery':{'status-data': battery}
    }
    
    return status_json or None


def last_access_log_query(limit, ip_filter=None):
    #parametros query
    selects = None
    
    columns = ['id', 'remote_host', 'date']
    
    if ip_filter:
        filter = access_log_table.columns.remote_host != f'{ip_filter}'
    else:
        filter = None
    
    order = access_log_table.columns.id.desc()


    resultados = access_log.query(selects=selects, columns=columns, filters=filter, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list


def most_accesses_by_ip_query(limit):
    time_threshold = datetime.utcnow() - timedelta(hours=24)

    #parametros query
    selects = [access_log_table.c.remote_host,func.count().label('count'),func.max(access_log_table.c.date).label('last_access')]
    columns = None
    filters = access_log_table.c.date >= time_threshold
    group = access_log_table.c.remote_host
    order = func.count().desc()
    
    resultados = access_log.query(selects=selects, columns=columns, filters=filters, group_by=group, order_by=order, limit=limit)
    
    resultados_list = [dict(row) for row in resultados]
    
    return resultados_list
