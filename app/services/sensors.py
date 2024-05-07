"""Related sensors functions."""
import time
from datetime import datetime
import csv

from app.services.net_and_connections import net_detect, make_get_request
from app.services.pushover_notifications import send_noti
from app.extensions import db
from models import SensorData

from config import THINKSPEAK_API_KEY

save_sensor_data = True


def sensor_data_db():
    s_data = SensorData.query.filter_by(sensor_name='sensor1').first()
    print('Error de db')

    return s_data.sensor_name, s_data.temperature, s_data.humidity, s_data.date, s_data.battery_level




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