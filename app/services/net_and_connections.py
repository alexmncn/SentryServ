"""Related net and device connections functions."""
import re, requests

from app.services.system import execute_command

from app.config import ESP32_PC_ON_KEY

ip_pc_piso = '192.168.1.68'
ip_pc_casa = '192.168.0.12'


def check_device_connection(ip_address):
    try:
        command = ['ping','-c', '1','-W','1', ip_address]
        ping = execute_command(command, use_shell=False)
        
        if "0% packet loss" in ping.stdout:
            return "Connected"
        else:
            return "Disconnected"
    except ping.CalledProcessError:
        return "Disconnected"
    
    
# Get local IP
def get_local_ip():
    try:
        command = ['hostname', '-I']
        ip = execute_command(command, use_shell=False).stdout.decode('utf-8').strip()
        return ip.split()[0]  # Take the first IP address from the list
    except Exception as e:
        print("Error getting local IP:", e)
        return None
    
    
def net_detect():
    ip = get_local_ip()
    octet_3 = 0
    if ip is not None:
        octet_3 = int(ip.split('.')[2])
        
    return octet_3

# Return the 3rd octet of the network ip.
def scan_network(ip_range):
    command = f'nmap -sn {ip_range}'
    result = execute_command(command)

    hosts_data = []

    if result.returncode == 0:
        # Extract IPs and hostnames using regular names
        pattern = re.compile(r'Nmap scan report for (.+) \((\d+\.\d+\.\d+\.\d+)\)')
        matches = pattern.findall(result.stdout)

        for match in enumerate(matches, start=1):
            host_name, ip = match
            hosts_data.append({'Host': host_name, 'IP': ip, 'Status':'Activo'})
    else:
        print(f'Error: {result.stderr}')
    return hosts_data


# Makes a get request to a specific address
def make_get_request(url):
    try:
        # Make request to the url
        response = requests.get(url)
            
        # Check and return the status code of the request
        if response.status_code == 200:
            return response.status_code, response
        else:
            return response.status_code, f'Error en la solicitud: {response.status_code}'
    except Exception as e:
        return None, f'Error en la solicitud: {e}'


# Check if PC is ON or OFF 
def pc_status():
    octet_3 = net_detect()
    
    if octet_3 == 0:
        ip_pc = ip_pc_casa
    else: ip_pc = ip_pc_piso

    return check_device_connection(ip_pc)


# Power on PC via ESP32 request
def pc_on_esp32():
    # Call net_detect funct. to know the 3rd octet of the network ip.
    octet_3 = net_detect()
    ip_esp = f'192.168.{octet_3}.100'

    url_web_esp_on = f'http://{ip_esp}/control?secret_class={ESP32_PC_ON_KEY}&on=ON'

    # Check the state of the pc and proceed as follows
    current_status = pc_status()

    if current_status == 'Conectado':
        return 'El PC ya está encendido'
    else:
        code, response = make_get_request(url_web_esp_on)

        if code == 200:
            return 'PC encendido corectamente'
        elif code == None:
            return response
        else:
            return f'No se ha podido encender el PC. {response}: {code}'
