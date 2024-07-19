import sys
import os
import time
import base64
from requests.auth import HTTPBasicAuth

# Get the path of the directory containing the 'app' module
app_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

# Add the path to sys.path
sys.path.append(app_path)

from app.services.net_and_connections import get_public_ip, make_get_request
from app.services.pushover_notifications import send_noti

from app.config import NOIP_DNS

last_public_IP = None


def detect_new_public_ip():
    global last_public_IP
    while True:
        public_IP = get_public_ip()
        
        if public_IP is not None:
            if public_IP != last_public_IP:
                last_public_IP = public_IP
                
                message = f'IP del servidor: {public_IP}'
                send_noti(message,'default')
                
                try:
                    result = update_ip_dns(public_IP)
                    if result:
                        message = 'Se ha actualizado la IP en el DNS.'
                    else:
                        message = 'La IP ya estaba actualizada.'
                    send_noti(message,'default')
                except Exception as e:
                    send_noti(f'Error al actualizar la IP automaticamente: {e}', 'default')
                    
            time.sleep(600)
        else:
            time.sleep(60)
        
    
    
def update_ip_dns(new_ip):
    url = NOIP_DNS.URL
    
    # Query parameters
    params = {
        'myip': new_ip,
        'hostname': NOIP_DNS.HOSTNAME,
    }
    
    # Creds base64 encode
    auth_str = f"{NOIP_DNS.USERNAME}:{NOIP_DNS.PASSWORD}"
    auth_bytes = auth_str.encode('ascii')
    base64_bytes = base64.b64encode(auth_bytes)
    base64_auth_str = base64_bytes.decode('ascii')
    
    # HTTP headers (include encoded creds in authorization header)
    headers = {
        'User-Agent': 'Python-Client/1.0',
        'Authorization': f'Basic {base64_auth_str}'
    }
    
    code, response = make_get_request(url, params=params, headers=headers)
    
    if code == 200:
        body = response.text.strip()
        if body.startswith("good "):
            return True
        elif body.startswith("nochg "):
            return False
        elif body == "nohost":
            raise Exception("NoHost")
        elif body == "badauth":
            raise Exception("BadAuth")
        elif body == "badagent":
            raise Exception("BadAgent")
        elif body == "!donator":
            raise Exception("NotDonator")
        elif body == "abuse":
            raise Exception("Abuse")
        elif body == "911":
            raise Exception("NineOneOne")
        else:
            raise Exception(f"Unknown error: {body}")
    elif code == 401:
        raise Exception("BadAuth")
    elif code == None:
        raise Exception(response)
    else:
        raise Exception(f"HTTP Error {response.status_code}: {response.reason}")
    

def main():
    detect_new_public_ip()


# Execute the main function
if __name__ == "__main__":
    main()