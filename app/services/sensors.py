"""Related sensors functions."""
import time
from datetime import datetime
import csv
from sqlalchemy import desc
import subprocess

from app.services.user import user_has_role
from app.extensions import db
from app.services.system import execute_command
from app.services.net_and_connections import net_detect, make_get_request
from app.services.pushover_notifications import send_noti
from app.models import SensorData

from app.config import THINKSPEAK_API_KEY

save_sensor_data = True


def sensor_data_db(sensor=1):
    sensor_name=f'sensor{sensor}'

    s_data = SensorData.query.filter_by(sensor_name=sensor_name).order_by(desc(SensorData.date)).first()
    
    if s_data is not None:
        return s_data.sensor_name, s_data.temperature, s_data.humidity, s_data.date, s_data.battery_level
    else:
        return None


def mqtt_app_control(action='status', option=None):
    def status():
        command = ['systemctl status mqtt_app.service']
        output = execute_command(command, use_shell=True)
    
        status = None
        since_date = None

        # Extract the data from the output
        for line in output.stdout.split('\n'):
            if 'Active:' in line:
                parts = line.split()
                status = parts[1] # Second word after 'Active' is the status
            
                # Date is after "since"
                since_index = line.find('since') + len('since')
                date_time = line[since_index:].strip().split(';')
            
                since_date = date_time[0]
                since_time = date_time[1]
                break
        
        return status, since_date, since_time
    
    @user_has_role('admin')
    def change_status(option):
        # Filter the action for command
        if option=='on':
            option='start'
        elif option=='off':
            option='stop'
        else:
            return 'Invalid command'
        
        # Save the previous status
        pre_status = status()

        command = [f'sudo systemctl {option} mqtt_app.service']

        # Ejecutar el comando
        execute_command(command, use_shell=True)        
        
        # Save the 'changed' status
        post_status = status()
        
        # Compare and return the result of the action
        if post_status != pre_status:
            return 'success'
        else:
            return 'error'

    
    if action=='status':
        return status()
    elif action=='change_status':
        return change_status(option)
    else:
        return None



# --------------------------------- CURRENTLY UNUSED -------------------------------------

# Obtiene y devuelve la temperatura y la humedad obtenida del sensor conectado al esp32
def temperature_and_humidity_dht22():
    octet_3 = net_detect()
    ip_esp = f'192.168.{octet_3}.100'

    url_web_esp_th = f'http://{ip_esp}/getTempAndHumd'
    
    code, response = make_get_request(url_web_esp_th)
    
    e = None

    if code == 200:
        data = response.json()

        temp = round(float(data["temperature"]), 1)
        humd = round(float(data["humidity"]), 1)
    else:
        code2, response2 = make_get_request(url_web_esp_th)
        
        if code2 == 200:
            data = response2.json()

            temp = round(float(data["temperature"]), 1)
            humd = round(float(data["humidity"]), 1)
        else:
            temp = None
            humd = None
            e = response2

    return temp, humd, e


# Llama a la funcion que devuelve los datos del sensor y los guarda cada 30 segundos en un .csv || NO USADA
def save_sensor_data_csv():
    time_delay = 60
    send_noti(f'Se ha empezado a guardar datos del sensor. Cada {time_delay} seg.', 'default')
    while save_sensor_data:
        try:
            temperature, humidity, e = temperature_and_humidity_dht22()

            fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
            # Guardar los datos en el archivo CSV
            with open('/var/www/html/logs/sensor_data.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([fecha, temperature, humidity])
        except:
            send_noti('Error al guardar datos.', 'default')

        # Pausa establecida por el time_delay entre insercciones
        time.sleep(time_delay)

    send_noti('Se ha parado el guardado de datos del sensor.', 'default')


# Enviamos datos del sensor a la web ThinkSpeak || NO USADA
def send_sensor_data_thinkspeak():
    time_delay = 60
    send_noti(f'Se ha empezado a enviar datos del sensor a ThinkSpeak.', 'default')

    while save_sensor_data:
        try:
            temperature, humidity, error = temperature_and_humidity_dht22()
            if temperature != None:
                url_thinkspeak_s1 = f'https://api.thingspeak.com/update?api_key={THINKSPEAK_API_KEY}&field1={temperature}&field2={humidity}'
                response = make_get_request.get(url_thinkspeak_s1)
            else:
                send_noti('No se han enviado datos a ThinkSpeak. Datos Nulos', 'default')
        except Exception as e:
            send_noti(f'Error al enviar datos a ThinkSpeak. {e}. {error}', 'default')

        # Pausa establecida por el time_delay entre cada envio
        time.sleep(time_delay)
        
    send_noti('Se ha parado de enviar datos al sensor.')
