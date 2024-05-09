"""MQTT save to Database service. Executed by system as a '.service'."""
import sys
import os

# Get the path of the directory containing the 'app' module
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Add the path to sys.path
sys.path.append(app_path)

import time
import threading
import json
import paho.mqtt.client as mqtt
from datetime import datetime

from app.app import create_app
from app.services.pushover_notifications import send_noti
from app.extensions import db 
from app.models import SensorData

from app.config import MQTT_Service

low_batt = False

# MQTT server configuration
MQTT_HOST = MQTT_Service.HOST
MQTT_PORT = MQTT_Service.PORT
MQTT_CLIENT_ID = MQTT_Service.CLIENT_ID
MQTT_KEEP_ALIVE = 60

TOPIC = MQTT_Service.TOPIC

# Path to CA certificate
CA_CERTIFICATE = MQTT_Service.CA_CERTIFICATE


def insert_sensor_data(sensor_name, temperature, humidity, date, battery_level):
    app = create_app()
    with app.app_context():
        new_data = SensorData(sensor_name=sensor_name, temperature=temperature, humidity=humidity, date=date, battery_level=battery_level)
        db.session.add(new_data)
        db.session.commit()


# Function to handle received messages
def on_message(client, userdata, message):
    # Get the message in JSON format
    message_data = json.loads(message.payload.decode())
    print(message_data)
    # Extract message data
    sensor_name = message_data["sensor"]
    temperature = message_data["temp"]
    humidity = message_data["humd"]
    date_str = message_data.get("date")
    date = datetime.strptime(date_str, "%d-%m-%Y %H:%M:%S") if date_str else None
    battery_level = message_data["battery"]

    # Insert data into the database
    try:
        insert_sensor_data(sensor_name, temperature, humidity, date, battery_level)
    except:
        send_noti("Error inserting data into DB from MQTT_Service.", 'default')

    # Send notification
    global low_batt
    if battery_level < 10 and low_batt is False:
        send_noti(f"Low Battery: {battery_level} %", 'default')
        low_batt = True


# Function to start MQTT client and subscribe to a topic
def start_mqtt_subscription():
    mqtt_client = mqtt.Client(client_id=MQTT_CLIENT_ID, clean_session=False)
    # mqtt_client.tls_set(CA_CERTIFICATE)

    mqtt_client.on_message = on_message
    mqtt_client.connect(MQTT_HOST, MQTT_PORT, MQTT_KEEP_ALIVE)
    # Subscribe to the topic
    mqtt_client.subscribe(TOPIC, qos=2)  # QoS 2 for exactly once delivery

    # Start receiving messages
    mqtt_client.loop_forever()


def main():
    start_mqtt_subscription()


# Execute the main function
if __name__ == "__main__":
    main()
