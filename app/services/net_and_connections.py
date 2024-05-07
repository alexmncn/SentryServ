"""Related net and device connections functions."""
from app.services.system import execute_command, get_local_ip

def check_device_connection(ip_address):
    try:
        command = ['ping','-c', '1','-W','1', ip_address]
        ping = execute_command(command)
        
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
        ip = execute_command(command).decode('utf-8').strip()
        return ip.split()[0]  # Take the first IP address from the list
    except Exception as e:
        print("Error getting local IP:", e)
        return None
    
    
def net_detect():
    ip = get_local_ip()
    if ip is not None:
        octet_3 = int(ip.split('.')[2])
        
    return octet_3 or 1


# Check if PC is ON or OFF 
def pc_status():
    octect_3 = net_detect()
    
    ip_pc_piso = '192.168.1.53'
    ip_pc_casa = '192.168.0.12'
    
    if octect_3 == 0:
        ip_pc = ip_pc_casa
    else: ip_pc = ip_pc_piso

    return check_device_connection(ip_pc)


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