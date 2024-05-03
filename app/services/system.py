"""System funct."""
import subprocess

# Execute script/command
def execute_command(command):
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True, encoding="utf-8")
        return output
    except subprocess.CalledProcessError as e:
        return e.output


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


def get_ram_usage():
    command = ['free', '-m']
    
    # Execute the 'free -m' command and capture the output
    output = execute_command(command)

    # Get output lines
    lines = output.stdout.split('\n')

    # Iterate through lines and extract CPU usage percentages
    for line in lines:
        # Split the line into columns
        columns = line.split()
        # Check if there are columns and if the first column is 'Mem:'
        if len(columns) > 0 and columns[0] == 'Mem:':
            ram_usage = int(columns[1]) - int(columns[6])

    return ram_usage


# Execute the command and obtain the total CPU usage
def get_cpu_usage():
    # Execute the 'sar -u' command and capture the output
    command = ['sar', '-u', '1', '1']
    output = execute_command(command)
    
    # Get the output lines
    lines = output.stdout.split('\n')

    # Initialize a list to store CPU usage percentages
    cpu_percentages = []

    # Iterate through the lines and extract CPU usage percentages
    for line in lines:
        # Split the line into columns
        columns = line.split()
        # Check if there are columns and if the first column is 'all'
        if len(columns) > 0 and columns[1] == 'all':

            for column in columns[2:7]:
                # Get the CPU usage percentage and convert it to float
                cpu_percentage = float(column)
                # Append the percentage to the list
                cpu_percentages.append(cpu_percentage)

    # Sum up the CPU usage percentages
    total_cpu_usage = sum(cpu_percentages)

    # Return the total CPU usage
    return total_cpu_usage


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
