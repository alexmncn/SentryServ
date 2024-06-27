import sys
import os
import time

# Get the path of the directory containing the 'app' module
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Add the path to sys.path
sys.path.append(app_path)

from app.services.net_and_connections import get_public_ip
from app.services.pushover_notifications import send_noti

init = True


def notify_new_public_ip():
    public_ip = get_public_ip()
    if public_ip is not None:
        send_noti(f'IP del servidor: {public_ip}','default')
    else:
        time.sleep(10000)
        notify_new_public_ip()


def main():
    notify_new_public_ip()


# Execute the main function
if __name__ == "__main__":
    main()
