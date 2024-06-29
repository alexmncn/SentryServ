import sys
import os
import time

# Get the path of the directory containing the 'app' module
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Add the path to sys.path
sys.path.append(app_path)

from app.services.net_and_connections import get_public_ip
from app.services.pushover_notifications import send_noti

last_public_IP = None

def notify_new_public_ip():
    global last_public_IP
    while True:
        public_IP = get_public_ip()
        
        if public_IP is not None:
            if public_IP != last_public_IP:
                last_public_IP = public_IP
                send_noti(f'IP del servidor: {public_IP}','default')
            time.sleep(3600)
        else:
            time.sleep(60)
        


def main():
    notify_new_public_ip()


# Execute the main function
if __name__ == "__main__":
    main()